import socket

IP_LIST = {"pi" : "##.##.##.##", "raspberrypi" : "##.##.##.##", "shortcake" : "##.##.##.##", "ANY" : "0.0.0.0"}
#pi and raspberry pi are the two pi 4s, shortcake is the pi 5, and ANY will let it recieve from any IP

class skynet:
    
    def __init__(self, host, IP, port, sim=False):
        self._host = host
        self._UDP_IP = IP
        self._UDP_Port = port
        if not sim:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
            if not self._host:
                self._sock.bind((self._UDP_IP, self._UDP_Port))
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
    
if __name__ == "__main__":
    sky = skynet(True, IP_LIST["raspberrypi"], 5005)
    import time
    print("starting loop")
    count = 1
    while True:
        count += 1
        if count % 2 == 1:
            sky.send(b"T")
        else:
            sky.send(b"F")

# recieving code example   
# if __name__ == "__main__":
#     sky = skynet(False, IP_LIST["ANY"], 5005)
#     from gpio import gpio, OUTPUT
#     g = gpio(4)
#     g.setMode(4, OUTPUT)
#     print("starting loop")
#     while True:
#         data = sky.recieve(1)
#         if (data == "T"):
#             print("running fan")
#             g.write(4, 1)
#         elif (data == "F"):
#             print("stopping fan")
#             g.write(4, 0)
