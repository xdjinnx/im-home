import sys

from listener import Listener

##
# Start point for application. Creates a listener for packages.
#
def main(ip, port, sendingPort):
    Listener(ip, port, sendingPort)

main(sys.argv[1], sys.argv[2], sys.argv[3])
