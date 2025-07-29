import subprocess
import threading
import os
import time
import sys
import signal
from multiprocessing import Process, Pipe
import psutil
import csv
import io
import math
from motors import Motor
from controlLoop import PID
import ctypes
import pathlib

class encoder():
    
    _s1 = subprocess
    _s2 = subprocess
    _pinA = -1
    _pinB = -1
    _state = ''
    _position = 0.0
    _velocity = 0.0
    _t1 = threading.Thread
    _t2 = threading.Thread
    _t3 = threading.Thread
    _procname = "Encoder"
    
    
    def __init__(self, pin1, pin2, RS, state):
        
        libname = pathlib.Path().absolute() / "Encoder.so"
        self._c_lib = ctypes.CDLL(libname)
        
        self._c_lib.readPosition.restype = ctypes.c_double
        self._c_lib.readVelocity.restype = ctypes.c_double
        
        self._running = True
        self._startTime = time.time()
        self._pinA = pin1
        self._pinB = pin2
        self._RS = RS
        self._state = state
        self._p1 = Process(target=self._runEncoder)
        self._p1.start()
    
    def _runEncoder(self):
        self._s1 = subprocess.Popen(["./Encoder", self._pinA, self._pinB, self._RS, self._state])

    def _updatePosition(self):
        pass

    def read(self):
        val = float(self._c_lib.readPosition())
        return val
    
    def readRad(self):
        return float(self.read()) * 6.283
    
    def readDeg(self):
        return float(self.read()) * 360
    
    def resetLogs(self):
        os.remove(r"/home/nick/LoCSST_DM/Logging.txt")
        
    def getVelocity(self):
        val = float(self._c_lib.readVelocity())
        return val
        
    def _reZero(self):
        pass
    
    def _getStepperPos(self):
        t_1 = time.time() - self._startTime
        v = self._velocity
        t_2 = 180 / v
        p = t_1 / t_2
        return math.floor(p * 180)
        
        
    def stop(self):
        pass

    def _standardQuit(self, signum, frame):
        self._running = False
        if self._p1.pid == None:
            raise RuntimeError("PID not found")
        os.kill(self._p1.pid, signal.SIGTERM)
        self._p1.join()
        for proc in psutil.process_iter():
            if proc.name() == self._procname:
                proc.kill()
        exit(0)


if __name__ == "__main__":
    en = encoder("4", "17", 'R', "5")
    mo = Motor()
    start = time.time()
    rotation = 0.0
    velocity = 0.0
    time_diff = 0.0
    mo.setSpeed(480)
    mo.enable()
    while True:
        rotation = en.read()
        velocity = en.getVelocity()
        time_diff = time.time() - start
        print(f"Rot: {rotation:.10} Vel: {velocity:.10} Time: {time_diff:.10}")
        time.sleep(0.5)
        
