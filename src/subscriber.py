
class subscriber():

    ##
    # This inits an object that is more or less a DTO.
    #
    # @param subIp The ip which is subbed for.
    # @param ip The Ip that has subbed.
    # @param port Responding port.
    # @param lastResponse Latest online response.
    #
    def __init__(self, subIp, ip, port, lastResponse):
        self.subIp = subIp
        self.ip = ip
        self.port = port
        self.lastResponse = lastResponse
