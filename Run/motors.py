import pigpio
import threading
import time
from gpio import gpio

MAX_SPEED = 480

class Motor(object):
    def __init__(self):
        
        self._pin_nEN = 3
        self._pin_nFAULT = 27
        self._pin_M1PWM = 18
        self._pin_M1DIR = 2
        self._gpio = gpio(5)
        self._gpio.setMode(self._pin_nEN, pigpio.OUTPUT)
        self._gpio.setMode(self._pin_nFAULT, pigpio.INPUT)
        self._gpio.setMode(self._pin_M1DIR, pigpio.OUTPUT)
        self._gpio.setMode(self._pin_M1PWM, pigpio.OUTPUT)
        
        self._gpio.setPUD(self._pin_nFAULT, pigpio.PUD_UP)
    def getFault(self):
        return not self._gpio.read(self.pin_nFAULT)

    def enable(self):
        self._gpio.write(self._pin_nEN, 0)

    def disable(self):
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
        
        # 20 kHz PWM, duty cycle in range 0-1000000 as expected by pigpio
        self._gpio.write(self._pin_M1DIR, dir_value)
        self._gpio.writePWM(self._pin_M1PWM, speed)


if (__name__ == "__main__"):
    motor = Motor()
    motor.enable()
    
    while True:
        motor.setSpeed(MAX_SPEED)
    motor.disable()
    
