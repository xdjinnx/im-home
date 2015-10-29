import os

##
# Checks if ip is online in lan.
#
# @param ip Ip that should be checked against lan.
#
def isReachable(ip):
    response = os.system("ping -c 1 " + ip)

    if response == 0:
        return 1
    return 0
