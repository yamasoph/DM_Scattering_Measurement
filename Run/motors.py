import pigpio
import threading
import time
from gpio import gpio
from skynet import skynet, IP_LIST, TIMEOUT

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

        # _pi.write(self._pin_M1DIR, dir_value)
        # _pi.set_PWM_dutycycle(self._pin_M1PWM, speed)
        #_pi.hardware_PWM(self.pwm_pin, 20000, int(speed * 6250 / 3))
        # 20 kHz PWM, duty cycle in range 0-1000000 as expected by pigpio
        self._gpio.write(self._pin_M1DIR, dir_value)
        self._gpio.writePWM(self._pin_M1PWM, speed)


class stepper(object):

    def __init__(self):
        self._position = 0.0
        self._dir = 0
        from skynet import skynet, IP_LIST
        self._sky = skynet(True, IP_LIST["raspberrypi"], 5005, sim=False)

    def enable(self):
        self._sky.updateSteps(other=["E"])
        self._sky.sendSteps()
    def disable(self):
        self._sky.updateSteps(other=["D"])
        self._sky.sendSteps()

    def setDir(self, direction):
        self._dir = direction
        self._sky.updateSteps(direction=self._dir)
        self._sky.sendSteps()

    #The local position will increase even if the motor is disabled so use remote position if you are commanding it while disabled

    def fullStep(self):
        self._sky.updateSteps(full=1)
        rval = self._sky.sendSteps()
        if self._dir:
            self._position += 1.8
        else:
            self._position -= 1.8
        return rval

    def halfStep(self):
        self._sky.updateSteps(half=1)
        rval = self._sky.sendSteps()
        if self._dir:
            self._position += 1.8 / 2
        else:
            self._position -= 1.8 / 2
        return rval

    def quarterStep(self):
        self._sky.updateSteps(quarter=1)
        rval = self._sky.sendSteps()
        if self._dir:
            self._position += 1.8 / 4
        else:
            self._position -= 1.8 / 4
        return rval

    def eighthStep(self):
        self._sky.updateSteps(eighth=1)
        rval = self._sky.sendSteps()
        if self._dir:
            self._position += 1.8 / 8
        else:
            self._position -= 1.8 / 8
        return rval

    def customStep(self, f=0, h=0, q=0, e=0, dir_value=-1, o=["A"]):#change the direction first this will only change it for upcoming steps
        if dir_value != -1:
            self._dir = dir_value
        self._sky.updateSteps(full=f, half=h, quarter=q, eighth=e, direction=self._dir, other=o)
        rval = self._sky.sendSteps()
        if self._dir:
            self._position += 1.8 * (f + (h / 2) + (q / 4) + (e / 8))
        else:
            self._position -= 1.8 * (f + (h / 2) + (q / 4) + (e / 8))
        return rval

    def getLocalPosition(self):
        return self._position

    def signalPosition(self):
        self._sky.updateSteps(other=["S"])
        return self._sky.sendSteps()

    def confirmConnection(self):
        self._sky.updateSteps(other=["!"])
        self._sky.sendSteps()

    # should always be very similar to local position the difference is floating point error
    # slower than grabbing the local position so not recommended 
    def getRemotePosition(self):
        for i in range(5):
            self._sky.updateSteps(other=["$"])
            self._sky.sendSteps()
            try:
                pos = float(self._sky.receive(10))
                break
            except (TIMEOUT, ValueError):
                print("timeout occured")
                pos = -99
        return pos

    def confirmPos(self):
        pos = self.getRemotePosition()
        return abs(pos - self._position) < 0.2

    def resetPos(self):
        self._position = self.getRemotePosition()

    # use this after you are finished, the stepper will stop recieving signals after it recieves this and close the loop so the logging file can be viewed
    def end(self):
        self._sky.updateSteps(other=["N"])
        self._sky.sendSteps()