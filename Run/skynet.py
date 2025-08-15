import socket
import json


IP_LIST = {"pi" : "##.##.##.##", "raspberrypi" : "##.##.##.##", "shortcake" : "##.##.##.##", "ANY" : "0.0.0.0"}
#pi and raspberry pi are the two pi 4s, shortcake is the pi 5, and ANY will let it recieve from any IP
TIMEOUT = socket.timeout

class skynet:

    #sim should only be true in testing
    def __init__(self, host, IP, port, sim=False, receiveIP=IP_LIST["ANY"], receivePort=5560):
        self._host = host
        self._UDP_IP = IP
        self._UDP_Port = port

        self._receiveIP = receiveIP
        self._receivePort = receivePort

        # The reason the steps are held as a dictionary is in case a step is missed
        # How it works is it will send a message that is a json string of the dictionary then the other pi will send back a confirmation and do the steps commanded
        # if the steps commanded are more than 1 of each than it will indicate it missed a step
        # I could not figure out how to do confirmations without this since a confirmation could be missed and another message would be sent

        self._steps = {1 : 0, 2 : 0, 4 : 0, 8 : 0, 'D' : 0, -1 : ["A"]}

        if not sim:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self._sock.settimeout(1)
            self._sock.bind((self._receiveIP, self._receivePort))
        self._sim = sim

    def send(self, message):
        if not self._sim:
            self._sock.sendto(message, (self._UDP_IP, self._UDP_Port))
        else:
            print(f"pretending to send data: {message}")

    def receive(self, buffer):
        if not self._sim:
            data, addr = self._sock.recvfrom(buffer)
            return data.decode()
        else:
            return "in sim"

    def updateSteps(self, full=0, half=0, quarter=0, eighth=0, direction=-1, other=["A"]):
        self._steps[1] += full
        self._steps[2] += half
        self._steps[4] += quarter
        self._steps[8] += eighth
        if direction != -1:
            self._steps['D'] = direction
        self._steps[-1] = other

    def sendSteps(self):
        data = json.dumps(self._steps).encode('utf-8')

        for i in range(5):
            try:
                self._sock.sendto(data, (self._UDP_IP, self._UDP_Port))
                message = self.receive(10)#could add logging here
                return message == "OK"
            except TIMEOUT:
                print("timeout occured")
        return False
    def receiveSteps(self, buffer):
        data, addr = self._sock.recvfrom(buffer)
        newSteps = json.loads(data.decode())
        l = []
        for key, value in self._steps.items():
            if newSteps[key] is not value:
                l.append((key, value - newSteps))
        self._steps = newSteps
        return l