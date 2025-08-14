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
        #self._c_lib = ctypes.CDLL('./getReading.so')
        
        self._c_lib.readPosition.restype = ctypes.c_double
        self._c_lib.readVelocity.restype = ctypes.c_double
        
        self._running = True
        self._startTime = time.time()
        self._pinA = pin1
        self._pinB = pin2
        self._RS = RS
        self._state = state
        #self._parentCom, self._childCom = Pipe()
        
        #self._t1 = threading.Thread(target=self._runEncoder)#, args=(self.stop_event,))
        #self._t2 = threading.Thread(target=self._runFeedback)
        # self._t3 = threading.Thread(target=self._updatePosition)
        #self._t1.start()
       
        #self._p1 = Process._Popen(["./new_Encoder", self._pinA, self._pinB, self._state], stdout=self._childCom, stderr=self._childCom, stdin=self._childCom, bufsize=1, universal_newlines=True)
        #self._p1 = Process(target=self._c_lib.start)
        self._p1 = Process(target=self._runEncoder)
        self._p1.start()
       
        #self._t1.start()
        # self._t2.start()
        #signal.signal(signal.SIGINT, self._standardQuit)
        # self._t3.start()
    
    def _runEncoder(self):#, stop_event):
        self._s1 = subprocess.Popen(["./Encoder", self._pinA, self._pinB, self._RS, self._state])
    
    # def _runFeedback(self):
    #     #self._s2 = subprocess.Popen(["./getPosition"], shell=True, stdout=subprocess.PIPE, stdin=DEVNULL, stderr=STDOUT)
    #     self._s2 = subprocess.Popen(["./getPosition"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, bufsize=1, universal_newlines=True)
    #     pass

    def _updatePosition(self):
        pass
        # self._position = self._c_lib.getPosition()
        # self._velocity = self._c_lib.getVelocity()
        # while self._running:
            
        #     reading = self._s1.stdout.readline().strip()
        #     #reading = self._stdout.readline().strip()
        #     #reading = self._parentCom.recv()
        #     print(reading)
        #     try:
        #         if reading[0] == 'p':
        #             self._position = float(reading[1:])
        #         elif reading [0] == 'v':
        #             self._velocity = float(reading[1:])
        #     except:
        #         pass

    def read(self):#in rotations
        val = float(self._c_lib.readPosition())
        #print("POS: ", val)
        return val
    
    def readRad(self):
        return float(self.read()) * 6.283
    
    def readDeg(self):
        return float(self.read()) * 360
    
    def _resetLogs(self):
        os.remove(r"/home/nick/LoCSST_DM/Logging.txt")
        
    def getVelocity(self):
        val = float(self._c_lib.readVelocity())
        #print("VEL: ", val)
        return val
        
    def _reZero(self):
        # os.kill(self._s1.pid, signal.SIGTERM)
        # self._t1.join()
        # self._t1 = threading.Thread(target=self._runEncoder)
        # self._t1.start()
        pass
    
    def _getStepperPos(self):#just an estimate since they are two independent systems
        t_1 = time.time() - self._startTime
        v = self._velocity
        #v = 0.25
        t_2 = 180 / v
        p = t_1 / t_2
        return math.floor(p * 180)
        
        
    def stop(self):
        # self._t3.join()
        # os.kill(self._s2.pid, signal.SIGTERM)
        # self._t2.join()
        # os.kill(self._p1.pid, signal.SIGTERM)
        # self._p1.join()
        # for proc in psutil.process_iter():
        #     if proc.name() == self._procname:
        #         proc.kill()
        os.kill(self._p1.pid, signal.SIGTERM)
        self._p1.join()
        for proc in psutil.process_iter():
            if proc.name() == self._procname:
                proc.kill()

    def _standardQuit(self, signum, frame):
        self._running = False
        os.kill(self._p1.pid, signal.SIGTERM)
        self._p1.join()
        for proc in psutil.process_iter():
            if proc.name() == self._procname:
                proc.kill()
        exit(0)

# if __name__ == "__main__":
#     print("---IN TESTING MODE---")
#     en = encoder("4", "17", 'S')
#     start = time.time()
#     curr = time.time()
   
#     maximum = 0.0
#     minimum = 5.0
#     count = 1
#     average = 0.0
#     os.remove(r"/home/nick/LoCSST_DM/data.csv")
    
#     mo = Motor()
#     # mo.setSpeed(0)
#     # mo.enable()
#     past_position = 0.0
#     pid = PID(90, 0.5, mo)
#     goal = 0.0
#     while time.time() - start < 10:
#         curr = time.time()
#         en.read()
#         temp = time.time() - curr
#         goal = 0.05
#         pid.driveAt(goal, en.getVelocity())
#         with open ('data.csv', 'a+', newline='') as file:
#             # position = en.read()
#             # t = time.time()
#             writer = csv.writer(file)
#             writer.writerow([curr - start, temp])
#             #writer.writerow([time.time(), en.read(), en.getVelocity(), goal])
#     #     if temp > maximum:
#     #         maximum = temp
#     #     if temp < minimum:
#     #         minimum = temp
        
#     #     average += (temp - average) / count
#     #     count += 1   
#     # print("Max: ", maximum, " Min: ", minimum, " Average: ", average, count) 
    
#     # countf = count
#     # count = 1
#     # start = time.time()
#     # while count < countf:
#     #     en.read()
#     #     count += 1
#     # print (time.time() - start)
    
#     en.stop()
#     mo.setSpeed(0)
#     mo.disable()   
#     print("Al fin")



if __name__ == "__main__":
    en = encoder("4", "17", 'R', "4")
    mo = Motor()
    start = time.time()
    rotation = 0.0
    velocity = 0.0
    time_diff = 0.0
    mo.setSpeed(480)
    mo.enable()
    # while True:
    for i in range(5):
        rotation = en.read()
        velocity = en.getVelocity()
        time_diff = time.time() - start
        print(f"Rot: {rotation:.10} Vel: {velocity:.10} Time: {time_diff:.10}")
        time.sleep(1)
    en.stop()
    while True:
        print("looping")
        time.sleep(1)
        