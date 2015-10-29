import socket
import ipreach
import time
import threading
from subscriber import subscriber

##
# subscription list.
subscribers = []

##
# Lock object for this module.
lock = threading.Lock()

##
# Adds subscription.
#
# @param subIp The ip which is subbed for.
# @param ip The Ip that has subbed.
# @param port Responding port.
#
def add(subIp, ip, port):
    lock.acquire()
    try:
        sub = subscriber(subIp, ip, port, str(ipreach.isReachable(subIp)))
        subscribers.append(sub)
        send(sub)

        if len(subscribers) == 1:
            sub_handler()
    finally:
        lock.release() # release lock, no matter what

# TODO: def remove(sub):

##
# Send status change to subscriber.
#
# @param sub Subscriber object.
# TODO: Encrypt package
#
def send(sub):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(sub.subIp + '#' + sub.lastResponse, (sub.ip, sub.port))

class sub_handler(threading.Thread):

    ##
    # Init subscription thread that checks the subscriptions.
    # SHOULD NOT BE USED. <code>add(subIp, ip, port)</code> inits this when when needed.
    #
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    ##
    # Thread function that check subscriptions.
    #
    # TODO: Don't check the same ip twice
    #
    def run(self):
        while 0 < len(subscribers):
            for sub in subscribers:
                isIpReachable = str(ipreach.isReachable(sub.subIp))
                if isIpReachable != sub.lastResponse:
                    sub.lastResponse = isIpReachable
                    send(sub)
            time.sleep(5)
