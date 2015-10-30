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
    # @param secret Secret that should be in message if responder should listen.
    #
    def __init__(self, data, addr, port, secret):
        self.data = data
        self.addr = addr[0]
        self.port = port
        self.secret = secret
        threading.Thread.__init__(self)
        self.start()

    ##
    # Thread function that repondes and reads package.
    #
    # TODO: Decrypt package
    #
    def run(self):
        if self.hasSecret():
            if not self.checkSecret(self.data):
                return

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
        return data.split('#')[0] == 'sub'

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

    ##
    # Check if secret in object is same as in string param
    #
    # @param data Socket package data.
    #
    def checkSecret(self, data):
        data = data.split('#')
        if len(data) > 2:
            return self.secret == data[2]
        return False

    ##
    # Check if object has secret
    #
    def hasSecret(self):
        return self.secret != ''
