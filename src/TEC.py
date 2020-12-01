class MeerstetterTEC:
    """
    Meerstetter TEC Abstract class.
    This class forms and interprets queries send and received as byte arrays.

    It can be put in any interface needed and is used by the implemented interfaces in this package.
    """

    def __init__(self, address = 0):

        #address
        if (type(address) == str):
            try:
                address = int(address)
            except:
                raise Exception("Could not convert address str into an int")
        if (type(address) == int):
            if (address < 0 or address > 255):
                raise Exception("Address argument is either below 0 or above 255")
            self.address = "{:02x}".format(address)
        else:
            raise Exception("Type of address is not int or str")

        #sequence number, is increased whenever a new request is made
        self.sequence_number = 5545

    def formSetCommand(self, number, channel, value):
        self._advanceSequenceNumber()
        command = "#{}{:04X}"

    def formReadCommand(self, number, channel):
        self._advanceSequenceNumber()
        command = "#{}{:04X}?VR{:04X}{:02X}".format(self.address, self.sequence_number, number, channel)
        return self._appendCRC(command.encode())

    def _appendCRC(self, command_str):
        crc = 0
        for b in command_str:
            crc = self._crcRound(crc, int(b))
        crc_str = "{:04X}".format(crc)
        return command_str + crc_str.encode()

    def _crcRound(self, crc, byt):
        genPoly = 0x1021
        uiCharShifted = (byt & 0x00FF) << 8
        crc = crc ^ uiCharShifted
        for _ in range(8):
            if ((crc & 0x8000) != 0):
                crc = (crc << 1) ^ genPoly
            else:
                crc = crc << 1
            crc = crc & 0xFFFF
        return crc
    
    def _advanceSequenceNumber(self):
        self.sequence_number = self.sequence_number + 1
        if (self.sequence_number > 65535):
            self.sequence_number = 0
