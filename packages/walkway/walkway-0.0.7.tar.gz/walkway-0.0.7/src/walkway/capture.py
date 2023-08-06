# 2021-07-31. Leonardo Molina.
# 2021-09-03. Last modified.

from .flexible import Flexible
from .scheduler import Scheduler
from pathlib import Path
from threading import Lock

import argparse
import cv2
import datetime
import json
import math
import numpy as np
import PySpin
import signal
import sys
import textwrap
import threading
import time

class Codec:
    Raw = 0
    MJPG = 1
    H264 = 2


class States:
    Started = 1
    Ended = 2


def getFlir(nodeMap, nodeName, getter=PySpin.CIntegerPtr):
    success = False
    exception = ""
    try:
        node = getter(nodeMap.GetNode(nodeName))
        if PySpin.IsAvailable(node):
            success = True
    except PySpin.SpinnakerException as ex:
        exception = str(ex)
        success = False
    if success:
        return node.GetValue()
    else:
        print("Error: Unable to get '%s'" % nodeName)
        if len(exception) > 0:
            print("  >>%s" % exception)
        return None
    

def setFlir(nodeMap, nodeName, value):
    success = False
    exception = ""
    
    if isinstance(value, str):
        getter = PySpin.CEnumerationPtr
        setter = lambda node, value : node.SetIntValue(node.GetEntryByName(value).GetValue())
    elif isinstance(value, bool):
        getter = PySpin.CBooleanPtr
        setter = lambda node, value : node.SetValue(value)
    elif isinstance(value, float):
        getter = PySpin.CFloatPtr
        setter = lambda node, value : node.SetValue(value)
    else:
        getter = PySpin.CIntegerPtr
        setter = lambda node, value : node.SetValue(value)
    
    try:
        node = getter(nodeMap.GetNode(nodeName))
        if PySpin.IsAvailable(node) and PySpin.IsWritable(node):
            setter(node, value)
            success = True
    except PySpin.SpinnakerException as ex:
        exception = str(ex)
        success = False
    if success:
        return True
    else:
        print("Error: Unable to set '%s' to '%s'" % (nodeName, str(value)))
        if len(exception) > 0:
            print("  >>%s" % exception)
        return False


def jsonFile(filename):
    if Path(filename).is_file():
        try:
            f = open(filename)
            json.load(f)
            f.close()
            return filename
        except json.JSONDecodeError as e:
            f.close()
            raise e
        except Exception as e:
            raise e
    else:
        raise FileNotFoundError(filename)


class Capture(object):
    """
    Capture high-framerate videos of a custom-made, CatWalk-like setup for mice using FLIR's BlackFly cameras.
    A video is saved to disk every time motion is detected.
    A configuration file in JSON format may be provided:
        {
            "locomotionThreshold": 0.05,
            "quiescenceThreshold": 0.01,
            "minDuration": 0.75,
            "maxDuration": 3.00,
            "speedThreshold": 2.00,
            "areaProportion": 0.25,
            "bufferSize": 10,
            "blurSize": [0.10, 0.10],
            "exposureTime": 1000,
            "gain": 15,
            "gamma": 0.8,
            "resolution": [1280, 200],
            "offset": [0, 412],
            "acquisitionFrameRate": 166,
            "outputFrameRate": 30
        }
        
    """
    
    
    @property
    def resolution(self):
        p = self.__private
        return p.resolution
    
    
    def __onKeyPress(self, event):
        p = self.__private
        key = event.key
        if key == 'q':
            p.running = False
            #sys.exit(0)
    
    
    def __onClose(self, event):
        p = self.__private
        p.running = False
        
        
    def __save(self, buffer, nFrames):
        p = self.__private
        filename = "WW-%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        frameRate = p.outputFrameRate
        if p.codec == Codec.Raw:
            option = PySpin.AVIOption()
            option.frameRate = frameRate
        elif p.codec == Codec.MJPG:
            option = PySpin.MJPGOption()
            option.frameRate = frameRate
            option.quality = 95
        elif p.codec == Codec.H264:
            option = PySpin.H264Option()
            option.frameRate = frameRate
            option.bitrate = 1000000
            option.width = self.resolution[0]
            option.height = self.resolution[1]
        
        recorder = PySpin.SpinVideo()
        recorder.Open(filename, option)

        b = len(buffer)
        a = max(0, b - nFrames)
        for i in range(a, b):
            recorder.Append(buffer[i])
        recorder.Close()
    
    
    def __resetBackground(self):
        p = self.__private
        p.background = cv2.createBackgroundSubtractorMOG2(history=math.ceil(p.processFrequency / p.speedThreshold), detectShadows=False)
    
    
    def __dispose(self):
        p = self.__private
        p.processScheduler.stop()
        p.processScheduler.join()
        if p.cameraInitiated:
            p.camera.EndAcquisition()
            p.camera.DeInit()
            del p.camera
            p.flirSystem.ReleaseInstance()
    
    
    def __capture(self):
        p = self.__private
        k = 0
        while p.running:
            try:
                flirImage = p.camera.GetNextImage(int(p.grabTimeout * 1000))
                if not flirImage.IsIncomplete():
                    if k % (p.acquisitionFrameRate // p.processFrequency) == 0:
                        with p.processLock:
                            p.processImage = flirImage.GetNDArray().copy()
                    with p.bufferLock:
                        p.buffer.append(flirImage.Convert(PySpin.PixelFormat_Mono8, PySpin.HQ_LINEAR))
                    flirImage.Release()
            except PySpin.SpinnakerException as ex:
                print("Error: %s" % ex)
            # Free-up space every so often.
            if k % (p.acquisitionFrameRate // p.bufferClipFrequency) == 0:
                with p.bufferLock:
                    n = len(p.buffer) - math.ceil(p.bufferSize * p.acquisitionFrameRate)
                    if n > 0:
                        del p.buffer[:n]
    
    
    def __onProcess(self):
        p = self.__private
        # Test for motion.
        ksize = (round(p.blurSize[1] * self.resolution[1]), round(p.blurSize[0] * self.resolution[0]))
        ksize = (ksize[0] + 1 if ksize[0] % 2 == 0 else ksize[0], ksize[1] + 1 if ksize[1] % 2 == 0 else ksize[1])
        with p.processLock:
            blurred = cv2.blur(src=p.processImage, ksize=ksize)
        change = p.background.apply(blurred).astype(bool) #shape = 1024x1280
        
        # Collapse height. A change for each x-pixel is reported when a proportion of y-pixels also change.
        line = change.sum(axis=0) > p.areaProportion * self.resolution[1]
        if p.lines.shape[0] < math.ceil(1 / 2 * p.processFrequency / p.speedThreshold):
            p.lines = np.vstack((p.lines, line))
        else:
            p.lines[:-1] = p.lines[1:]
            p.lines[-1] = line
            p.trail = p.lines.any(axis=0)
            
            motionScore = p.trail.sum()
            motionDuration = time.time() - p.motionStart
            save = False
            if p.motionState == States.Ended and motionScore > p.locomotionThreshold * p.resolution[0]:
                # Acceleration: high-count-lines are pushed while low-count-lines are popped.
                print("Motion started... ", end='')
                p.motionState = States.Started
                p.motionStart = time.time()
            elif p.motionState == States.Started and motionScore < p.quiescenceThreshold * p.resolution[0]:
                    # Deceleration: low-count-lines are pushed while high-count-lines are popped.
                    if motionDuration > p.minDuration:
                        # Movement lasted enough.
                        self.__setMessage("Motion detected! duration:%.2fs" % motionDuration)
                        print("accepted! duration:%.2fs" % motionDuration)
                        save = True
                    else:
                        print("ignored! Too short. duration:%.2fs" % motionDuration)
                    p.motionState = States.Ended
            elif p.motionState == States.Started and motionDuration > p.maxDuration:
                    # Movement has lasted long enough; force save.
                    self.__setMessage("Motion detected! duration:%.2fs" % motionDuration)
                    print("accepted! Splitted. duration:%.2fs" % motionDuration)
                    p.motionState = States.Ended
                    save = True
            # Save on background.
            if save:
                nFrames = math.ceil((time.time() - p.motionStart) * p.acquisitionFrameRate)
                with p.bufferLock:
                    buffer = p.buffer.copy()
                threading.Thread(target=self.__save, args=(buffer, nFrames)).start()
    
    
    def start(self):
        p = self.__private
        
        p.flirSystem = PySpin.System.GetInstance()
        cameraList = p.flirSystem.GetCameras()
        
        if cameraList.GetSize() == 0:
            cameraList.Clear()
            p.flirSystem.ReleaseInstance()
            print("Error: Camera not connected. Aborting...")
            return False
            
        p.camera = cameraList[0]
        cameraList.Clear()
        try:
            p.camera.Init()
            nodemap = p.camera.GetNodeMap()
            sNodemap = p.camera.GetTLStreamNodeMap()
        except PySpin.SpinnakerException as ex:
            print("Error: %s" % ex)
            return False
        
        success = True
        success &= setFlir(sNodemap, "StreamBufferHandlingMode", "NewestOnly")
        success &= setFlir(nodemap, "AcquisitionMode", "Continuous")
        success &= setFlir(nodemap, "ExposureAuto", "Off")
        success &= setFlir(nodemap, "GainAuto", "Off")
        if p.exposureTime is not None:
            success &= setFlir(nodemap, "ExposureTime", float(p.exposureTime))
        if p.gain is not None:
            success &= setFlir(nodemap, "Gain", float(p.gain))
        if p.gamma is not None:
            success &= setFlir(nodemap, "GammaEnable", True)
            success &= setFlir(nodemap, "Gamma", float(p.gamma))
        if p.resolution is not None:
            success &= setFlir(nodemap, "Width", int(p.resolution[0]))
            success &= setFlir(nodemap, "Height", int(p.resolution[1]))
        if p.offset is not None:
            success &= setFlir(nodemap, "OffsetX", int(p.offset[0]))
            success &= setFlir(nodemap, "OffsetY", int(p.offset[1]))
        if p.acquisitionFrameRate is not None:
            success &= setFlir(nodemap, "AcquisitionFrameRateEnable", True)
            success &= setFlir(nodemap, "AcquisitionFrameRate", float(p.acquisitionFrameRate))
        
        p.acquisitionFrameRate = getFlir(nodemap, "AcquisitionFrameRate", getter = PySpin.CFloatPtr)
        success &= p.acquisitionFrameRate is not None
        
        if success:
            try:
                p.camera.BeginAcquisition()
            except PySpin.SpinnakerException as ex:
                print("Error: %s" % ex)
                success = False
        p.cameraInitiated = success
        
        if success:
            p.resolution = (getFlir(nodemap, "Width"), getFlir(nodemap, "Height"))
            
            # Collapse height.
            p.lines = np.empty((0, self.resolution[0]))
            p.trail = np.full(self.resolution[0], False)
            p.processImage = np.zeros((self.resolution[1], self.resolution[0]), np.uint8)
            
            # Start capturing.
            p.thread = threading.Thread(target=self.__capture, args=())
            p.thread.start()
            
            # Start processing.
            p.processScheduler.repeat(interval=1.0 / p.processFrequency)
            
            while p.running:
                with p.processLock:
                    frame = p.processImage.copy()
                margin = int(self.resolution[1] * p.margin)
                frame[0:margin, p.trail] = 0
                frame[-margin:-1, p.trail] = 0
                if time.time() < p.messageToc:
                    self.__showMessage(frame, *p.message[0], **p.message[1])
                cv2.imshow("image", frame)
                key = cv2.waitKey(1000 // p.processFrequency) & 0xFF
                if key == ord('q'):
                    p.running = False
            p.thread.join()
        
        self.__dispose()
        return success
    
    
    def __setMessage(self, *args, duration=1, **kwargs):
        p = self.__private
        p.messageToc = time.time() + duration
        p.message[0] = args
        p.message[1] = kwargs
        
        
    def __showMessage(self, image, text, center=(10, 30), color=50, fontScale=1):
        cv2.putText(
            img=image,
            text=text,
            org=center,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=fontScale,
            color=color,
            thickness=3
        )
        cv2.putText(
            img=image,
            text=text,
            org=center,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=fontScale,
            color=255,
            thickness=1
        )
    
    
    def __onKillSignal(self):
        p = self.__private
        p.running = False
        
        
    def __init__(self, **kwargs):
        p = self.__private = Flexible()
        
        # Locomotion starts when the number of active x-pixels is larger than k * width.
        p.locomotionThreshold = 0.05
        # Locomotion stops when the number of active x-pixels is smaller than k * width.
        p.quiescenceThreshold = 0.01
        # Videos are not saved if they last less than k seconds.
        p.minDuration = 0.75
        # Videos are split if they last longer than k seconds.
        p.maxDuration = 3.00
        # Speed threshold to detect motion (length-proportion/s).
        p.speedThreshold = 2.00
        # Proportion of y-pixels required to activate an x-pixel.
        p.areaProportion = 0.25
        # Other.
        p.bufferSize = 10
        p.blurSize = (0.10, 0.10)
        p.exposureTime = None
        p.gain = None
        p.gamma = None
        p.resolution = None
        p.offset = None
        p.acquisitionFrameRate = None
        p.outputFrameRate = 30
        
        p.codec = Codec.MJPG
        p.renderFrequency = 30
        p.processFrequency = 30
        p.bufferClipFrequency = 1
        
        p.margin = 0.05
        p.grabTimeout = 1.0
        
        # State variables.
        p.running = True
        p.motionStart = time.time()
        p.motionState = States.Ended
        p.messageToc = 0
        p.message = [[], {}]
        p.bufferLock = Lock()
        p.processLock = Lock()
        p.buffer = list()
        
        public = list([
            "locomotionThreshold",
            "quiescenceThreshold",
            "minDuration",
            "maxDuration",
            "speedThreshold",
            "areaProportion",
            "bufferSize",
            "blurSize",
            "exposureTime",
            "gain",
            "gamma",
            "resolution",
            "offset",
            "outputFrameRate",
            "acquisitionFrameRate"
        ])
        
        kwargs = {key: value for key, value in kwargs.items() if key in public}
        for key, value in kwargs.items():
            p.set(key, value)
        
        p.processScheduler = Scheduler()
        p.processScheduler.subscribe(lambda scheduler: self.__onProcess())
        self.__resetBackground()
        
        signal.signal(signal.SIGINT, lambda sig, frame: self.__onKillSignal())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.__onKillSignal())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=Capture.__doc__, formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('--configuration', type=jsonFile, help="Configuration file in JSON format")
    args = parser.parse_args()
    
    kwargs = {}
    if args.configuration is not None:
        with open(args.configuration) as f:
            kwargs = json.load(f)
    result = Capture(**kwargs).start()
    
    sys.exit(int(result))