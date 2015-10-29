import socket
import threading
import ipreach
import subscription_handler

class Responder(threading.Thread):

    ##
    # Init a responder that starts a thread, which handles and respond to the package.
    #
    # @param data Udp package data received from socket.
    # @param addr Ip that should be used as respond ip.
    # @param port Respond port.
    #
    def __init__(self, data, addr, port):
        self.data = data
        self.addr = addr[0]
        self.port = port
        threading.Thread.__init__(self)
        self.start()

    ##
    # Thread function that repondes and reads package.
    #
    # TODO: Decrypt package, listen for secret
    #
    def run(self):
        if self.isSubscription(self.data):
            subscription_handler.add(self.getSubIP(self.data), self.addr, self.port)
            self.send(self.getSubIP(self.data), 'subbed')
        else:
            self.send(self.data, str(ipreach.isReachable(self.data)))

    ##
    # Checks if package is a subscription message.
    #
    # @param data Socket package data.
    #
    def isSubscription(self, data):
        if data.split('#')[0] == 'sub':
            return True
        return False

    ##
    # Sending package as reponse.
    #
    # @param ip Ip that should be in the message. NOT RESPOND IP.
    # @param msg Message that should be sent with ip.
    # TODO: Encrypt package
    #
    def send(self, ip, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(ip + '#' + msg, (self.addr, self.port))

    ##
    # Get the ip that message want to sub to.
    #
    # @param data Socket package data.
    #
    def getSubIP(self, data):
        return data.split('#')[1]
