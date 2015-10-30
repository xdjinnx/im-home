import sys

from listener import Listener

##
# Start point for application. Creates a listener for packages.
#
def main(ip, port, sendingPort, secret = ''):
    Listener(ip, port, sendingPort, secret)

try:
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
except IndexError:
    main(sys.argv[1], sys.argv[2], sys.argv[3])
