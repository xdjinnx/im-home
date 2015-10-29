import socket
import threading
from responder import Responder

class Listener(threading.Thread):

    ##
    # Init a listener that listen on udp packages on port specifide as param.
    # This class does not handle the packages, it creates responders.
    #
    # @param ip Specifide ip as string that should be related to the application.
    # @param port listening port as string.
    # @param sendingPort port that application uses to send packages as string.
    #
    def __init__(self, ip, port, sendingPort):
        self.ip = ip
        self.port = int(port)
        self.sendingPort = int(sendingPort)
        threading.Thread.__init__(self)
        self.start()
        self.join()

    ##
    # Thread function. listens for packages and creates responders for does packages.
    #
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip, self.port))
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            Responder(data, addr, self.sendingPort)
