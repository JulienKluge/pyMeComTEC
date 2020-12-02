class MeerstetterTEC:
    """
    Meerstetter TEC Abstract class.
    This class forms and interprets queries send and received as byte arrays.

    It can be put in any interface needed and is used by the implemented interfaces in this package.
    """

    def __init__(self, tec_address = 0, check_crc = True):

        #address
        if (type(tec_address) == str):
            try:
                tec_address = int(tec_address)
            except:
                raise Exception("Could not convert address str into an int")
        if (type(tec_address) == int):
            if (tec_address < 0 or tec_address > 255):
                raise Exception("Address argument is either below 0 or above 255")
            self.tec_address = "{:02x}".format(tec_address)
        else:
            raise Exception("Type of address is not int or str")

        #sequence number, is increased whenever a new request is made
        self.sequence_number = -1
        self.check_crc = check_crc
    
    def _formIdentificationCommand(self):
        self._advanceSequenceNumber()
        command = "#{}{:04X}?IF".format(self.tec_address, self.sequence_number)
        return self._appendCRC(command.encode())

    def _formSetCommand(self, number, channel, value):
        self._advanceSequenceNumber()
        command = "#{}{:04X}"

    def _formReadCommand(self, number, channel):
        self._advanceSequenceNumber()
        command = "#{}{:04X}?VR{:04X}{:02X}".format(self.tec_address, self.sequence_number, number, channel)
        return self._appendCRC(command.encode())

    def _appendCRC(self, command_str):
        return command_str + self.form_crc(command_str)

    def form_crc(self, command_str):
        crc = 0
        for b in command_str:
            crc = self._crcRound(crc, int(b))
        crc_str = "{:04X}".format(crc)
        return crc_str.encode()

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
    
    def _validate_answer(self, answer):
        if (not self.check_crc):
            return True
        body_arr = answer[:-4]
        test_crc = answer[-4:]
        calc_crc = self.form_crc(body_arr)
        if (test_crc != calc_crc):
            raise Exception("Mismatch in checksums.")
        return True
    
    def _extract_payload(self, answer):
        return answer[7:-4]
    

    #
    #
    # public functions
    #
    #
    

    def get_id(self):
        command = self._formIdentificationCommand()
        answer = self._sendAndReceive(command)
        self._validate_answer(answer)
        id_str = self._extract_payload(answer)
        return id_str.decode()
    
    def get_value(self):
        raise NotImplementedError()
    def set_value(self):
        raise NotImplementedError()
    

    #
    #
    # inheritance functions
    #
    #


    def _sendAndReceive(self, byteArr):
        raise NotImplementedError()
    
