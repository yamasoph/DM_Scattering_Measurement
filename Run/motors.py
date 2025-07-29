import pigpio
import threading
import time
from gpio import gpio

# _pi = pigpio.pi()

# if not _pi.connected:
#     print("ERROR")
#     raise IOError("Can't connect to pigpio")

MAX_SPEED = 480



class Motor(object):
   

    def __init__(self):
        
        self._pin_nEN = 3
        self._pin_nFAULT = 27
        self._pin_M1PWM = 18
        self._pin_M1DIR = 2
        # _pi.set_mode(self._pin_nEN, pigpio.OUTPUT)
        # _pi.set_mode(self._pin_nFAULT, pigpio.INPUT)
        # _pi.set_mode(self._pin_M1DIR, pigpio.OUTPUT)
        # _pi.set_mode(self._pin_M1PWM, pigpio.OUTPUT)
        
        # _pi.set_pull_up_down(self._pin_nFAULT, pigpio.PUD_UP)
        self._gpio = gpio(5)
        self._gpio.setMode(self._pin_nEN, pigpio.OUTPUT)
        self._gpio.setMode(self._pin_nFAULT, pigpio.INPUT)
        self._gpio.setMode(self._pin_M1DIR, pigpio.OUTPUT)
        self._gpio.setMode(self._pin_M1PWM, pigpio.OUTPUT)
        
        self._gpio.setPUD(self._pin_nFAULT, pigpio.PUD_UP)
    def getFault(self):
        # return not _pi.read(self._pin_nFAULT)
        return not self._gpio.read(self._pin_nFAULT)

    def enable(self):
        # _pi.write(self._pin_nEN, 0)
        self._gpio.write(self._pin_nEN, 0)

    def disable(self):
        # _pi.write(self._pin_nEN, 1)
        self._gpio.write(self._pin_nEN, 1)
        
    def setNorm(self, speed):
        self.setSpeed(speed * MAX_SPEED)


    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 1
        else:
            dir_value = 0

        if speed > MAX_SPEED:
            speed = MAX_SPEED
        
        # _pi.write(self._pin_M1DIR, dir_value)
        # _pi.set_PWM_dutycycle(self._pin_M1PWM, speed)
        #_pi.hardware_PWM(self.pwm_pin, 20000, int(speed * 6250 / 3))
        # 20 kHz PWM, duty cycle in range 0-1000000 as expected by pigpio
        self._gpio.write(self._pin_M1DIR, dir_value)
        self._gpio.writePWM(self._pin_M1PWM, speed)
        
class stepper(object):
    
    def __init__(self):
        self._position = 0.0
        self._dir = False
        from skynet import skynet, IP_LIST
        self._sky = skynet(True, IP_LIST["raspberrypi"], 5005, sim=True)
    
    def enable(self):
        self._sky.send(b"E")
    def disable(self):
        self._sky.send(b"D")
    
    def changeDir(self, direction):
        self._dir = direction
        self._sky.send(b"C")
    
    def fullStep(self):
        self._sky.send(b"1")
        if self._dir:
            self._position += 1.8
        else:
            self._position -= 1.8
        
    def halfStep(self):
        self._sky.send(b"2")
        if self._dir:
            self._position += 1.8 / 2
        else:
            self._position -= 1.8 / 2
            
    def quarterStep(self):
        self._sky.send(b"4")
        if self._dir:
            self._position += 1.8 / 4
        else:
            self._position -= 1.8 / 4
            
    def eightStep(self):
        self._sky.send(b"8")
        if self._dir:
            self._position += 1.8 / 8 
        else:
            self._position -= 1.8 / 8
        
    def getPositionDeg(self):
        return self._position


if (__name__ == "__main__"):
    motor = Motor()
    motor.enable()
    
    while True:
        # for i in range(MAX_SPEED):
        #     motor.setSpeed(i)
        #     time.sleep(0.05)
        #     print(motor.getFault())
        #     print(i)
        # for i in range(MAX_SPEED):
        #     motor.setSpeed(-1 * i)
        #     time.sleep(0.05)
        #     print(motor.getFault())
        #     print(-1 * i)
        motor.setSpeed(MAX_SPEED)
    motor.disable()
    
