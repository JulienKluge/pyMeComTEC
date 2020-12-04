from struct import pack, unpack

import TEC_autogen
from TEC_Helper import MeComError, MeComException, MeParFlags, MeParType, MeCom_DriverStatus, MeCom_TemperatureStability

"""
Meerstetter TEC Abstract class.
This class forms and interprets queries send and received as byte arrays.

It can be put in any interface needed and is used by the implemented interfaces in this package.
"""
class MeerstetterTEC(TEC_autogen._MeerstetterTEC_autogen):

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
    
    def _compose_emergencystop_frame(self):
        self._advance_sequence_number()
        frame = "#{}{:04X}ES".format(self.tec_address,
            self.sequence_number
        )
        return self._appendCRC(frame.encode())

    def _compose_reset_frame(self):
        self._advance_sequence_number()
        frame = "#{}{:04X}RS".format(
            self.tec_address,
            self.sequence_number
        )
        return self._appendCRC(frame.encode())
    
    def _compose_identification_frame(self):
        self._advance_sequence_number()
        frame = "#{}{:04X}?IF".format(
            self.tec_address,
            self.sequence_number
        )
        return self._appendCRC(frame.encode())
    
    def _compose_metadata_frame(self, mepar_id, channel):
        self._advance_sequence_number()
        frame = "#{}{:04X}?VM{:04X}{:02X}".format(
            self.tec_address,
            self.sequence_number,
            mepar_id,
            channel
        )
        return self._appendCRC(frame.encode())

    def _compose_set_frame(self, mepar_id, channel, value):
        self._advance_sequence_number()
        frame = "#{}{:04X}VS{:04X}{:02X}{}".format(
            self.tec_address,
            self.sequence_number,
            mepar_id,
            channel,
            value
        )
        return self._appendCRC(frame.encode())

    def _compose_read_frame(self, mepar_id, channel):
        self._advance_sequence_number()
        frame = "#{}{:04X}?VR{:04X}{:02X}".format(
            self.tec_address,
            self.sequence_number,
            mepar_id,
            channel
        )
        return self._appendCRC(frame.encode())
    
    def _compose_bigread_frame(self, mepar_id, channel, read_start, max_nr_read):
        self._advance_sequence_number()
        frame = "#{}{:04X}?VB{:04X}{:02X}{:08X}{:04X}".format(
            self.tec_address,
            self.sequence_number,
            mepar_id,
            channel,
            read_start,
            max_nr_read
        )
        return self._appendCRC(frame.encode())

    def _compose_bigset_frame(self, mepar_id, mepar_type, channel, data, read_start = 0):
        if (type(data) == str):
            data = "".join(["{:02X}".format(b) for b in (data + "\x00").encode("LATIN-1")])
        data_length = len(data) * mepar_type.get_type_hex_length()
        if (data_length > (232 - 32)): #232bytes is the max which can be send over
            raise Exception("Too much data for a single frame was attempted to be sent")
        data_str = []
        for i in data:
            data_str += mepar_type.from_type(i)
        self._advance_sequence_number()
        frame = "#{}{:04X}VB{:04X}{:02X}{:08X}{:04X}01{}".format(
            self.tec_address,
            self.sequence_number,
            mepar_id,
            channel,
            read_start,
            len(data),
            "".join(data_str)
        )
        return self._appendCRC(frame.encode())

    def _appendCRC(self, frame_str):
        return frame_str + self.form_crc(frame_str)

    def form_crc(self, frame_str):
        crc = 0
        for b in frame_str:
            crc = self._crc_round(crc, int(b))
        crc_str = "{:04X}".format(crc)
        return crc_str.encode()

    def _crc_round(self, crc, byt):
        genPoly = 0x1021
        uiCharShifted = (byt & 0x00FF) << 8
        crc = crc ^ uiCharShifted
        for _ in range(8):
            if ((crc & 0x8000) != 0):
                crc = (crc << 1) ^ genPoly
            else:
                crc = crc << 1
            crc = crc & 0xFFFF
        return crc & 0xFFFF
    
    def _advance_sequence_number(self):
        self.sequence_number = self.sequence_number + 1
        if (self.sequence_number > 65535):
            self.sequence_number = 0
    
    def _validate_answer(self, answer, overwrite_checksum = ""):
        body_arr = answer[:-4]
        test_crc = answer[-4:]
        error_indicator = body_arr[-3]
        if (error_indicator == 43): #i don't know either why indexing in a byte array gives me an int... 43==b'+'
            error_number = int(body_arr[-2:], 16)
            raise MeComException(error_number)

        if (not self.check_crc):
            return True
        if (overwrite_checksum == ""):
            calc_crc = self.form_crc(body_arr)
        else:
            calc_crc = overwrite_checksum
        if (test_crc != calc_crc):
            raise Exception("Mismatch in checksums.")
        return True
    
    def _extract_payload(self, answer):
        return answer[7:-4]
    
    def _extract_metadata_payload(self, answer):
        payload = answer[7:-4]
        mepar_type = MeParType(int(payload[0:2], 16))
        mepar_flag = MeParFlags(int(payload[2:4], 16))
        instance_nr = int(payload[4:6], 16)
        max_nr = int(payload[6:14], 16)
        rest_payload = payload[14:]
        if (len(rest_payload) > 0):
            (field_type_length, field_type_mod) = divmod(len(rest_payload), 3)
            if (field_type_mod != 0):
                raise Exception("Field type lengths not a multiple of three")
            min_value = mepar_type.interpret_type(rest_payload[0:field_type_length])
            max_value = mepar_type.interpret_type(rest_payload[field_type_length:(field_type_length * 2)])
            act_value = mepar_type.interpret_type(rest_payload[(field_type_length * 2):(field_type_length * 3)])
            return (mepar_type, mepar_flag, instance_nr, max_nr, min_value, max_value, act_value)
        else:
            return (mepar_type, mepar_flag, instance_nr, max_nr, 0, 0, 0)
    
    def _extract_bigdata_payload(self, answer, mepar_type):
        payload = answer[7:-4]
        received_nr = int(payload[0:4], 16)
        has_more_data = int(payload[4:6], 16)
        data = payload[6:]
        if (len(data) > 0):
            data_l = mepar_type.get_type_hex_length()
            (field_type_length, field_type_mod) = divmod(len(data), data_l)
            if (field_type_length == received_nr and field_type_mod == 0):
                if (mepar_type == MeParType.LATIN1):
                    cleaned_string = (data.decode()).rstrip("\x00").rstrip("00")
                    return bytearray.fromhex(cleaned_string).decode("LATIN-1")
                else:
                    out_fields = []
                    for i in range(0, field_type_length):
                        payload_seq = data[(i * data_l):((i + 1) * data_l)]
                        out_fields += mepar_type.interpret_type(payload_seq)
                    return mepar_type._finish_bigdata_array(out_fields)
            else:
                raise Exception("Field type do not match counts or lengths not a multiple of data type length")
        else:
            return (received_nr, has_more_data, 0)
    #
    #
    # public functions
    #
    #
    
    """
    Disables all Power Outputs immediately and the Error 11 is generated.
    """
    def execute_emergency_stop(self, fire_and_forget = False):
        frame = self._compose_emergencystop_frame()
        if (fire_and_forget or self.tec_address == 255):
            self._send_and_ignore_receive(frame)
            return b''
        else:
            answer = self._send_and_receive(frame)
            self._validate_answer(answer, overwrite_checksum = frame[-4:])
            payload = self._extract_payload(answer)
            return payload == b''


    """
    Resets and thus restarts the device. The connection could be closed depending on the interface
    """
    def execute_reset(self, fire_and_forget = False):
        frame = self._compose_reset_frame()
        if (fire_and_forget or self.tec_address == 255):
            self._send_and_ignore_receive(frame)
            return b''
        else:
            answer = self._send_and_receive(frame)
            self._validate_answer(answer, overwrite_checksum = frame[-4:])
            payload = self._extract_payload(answer)
            return payload == b''


    """
    Reads the firmware identification string of the TEC. The returns always contains 20 character wherein
    the last are usually whitespace.
    """
    def read_firmware_id(self):
        frame = self._compose_identification_frame()
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        id_str = self._extract_payload(answer)
        return id_str.decode()


    """
    Reads the available metadata for a specified MeParID
    """
    def read_metadata(self, mepar_id, channel):
        frame = self._compose_metadata_frame(mepar_id, channel)
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        return self._extract_metadata_payload(answer)
    

    """
    Reads the value of a specified MeParID and converts it to the specified type
    """
    def read_value(self, mepar_id, mepar_type, channel):
        frame = self._compose_read_frame(mepar_id, channel)
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        payload = self._extract_payload(answer)
        return mepar_type.interpret_type(payload)


    """
    Reads the value of a specified MeParID and converts it to the specified type. Uses the big data
    command which is used for text or list data
    """
    def read_big_value(self, mepar_id, mepar_type, channel, read_start = 0, max_nr_read = 0xFFFF):
        frame = self._compose_bigread_frame(mepar_id, channel, read_start, max_nr_read)
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        payload = self._extract_bigdata_payload(answer, mepar_type)
        return payload #TODO parse further
    

    """
    Writes the given value to a specified MeParID
    """
    def write_value(self, mepar_id, mepar_type, raw_value, channel, fire_and_forget = False):
        value = mepar_type.from_type(raw_value)
        frame = self._compose_set_frame(mepar_id, channel, value)
        if (fire_and_forget or self.tec_address == 255):
            self._send_and_ignore_receive(frame)
            return True
        else:
            answer = self._send_and_receive(frame)
            self._validate_answer(answer, overwrite_checksum = frame[-4:])
            payload = self._extract_payload(answer)
            return payload == b''
    

    """
    Writes the given value to a specified MeParID as a bigdata
    """
    def write_big_value(self, mepar_id, mepar_type, value, read_start = 0, channel = 1, fire_and_forget = False):
        frame = self._compose_bigset_frame(mepar_id, mepar_type, channel, value, read_start)
        if (fire_and_forget or self.tec_address == 255):
            self._send_and_ignore_receive(frame)
            return True
        else:
            answer = self._send_and_receive(frame)
            self._validate_answer(answer, overwrite_checksum = frame[-4:])
            payload = self._extract_payload(answer)
            return payload == b''


    #
    #
    # Convenience functions
    #
    #
    def temperature(self, channel = 1):
        return self.TEC_ObjectTemperature(channel = channel)
        
    def nomimal_temperature(self, channel = 1):
        return self.TEC_RampNominalObjectTemperature(channel = channel)

    def target_temperature(self, channel = 1):
        return self.TEC_TargetObjectTemp(channel = channel)
    def write_target_temperature(self, value, channel = 1):
        return self.Set_TEC_TargetObjectTemp(value, channel = channel, fire_and_forget = False)

    def current(self, channel = 1):
        return self.TEC_ActualOutputCurrent(channel = channel)
        
    def voltage(self, channel = 1):
        return self.TEC_ActualOutputVoltage(channel = channel)
    
    def status(self, channel = 1):
        return MeCom_DriverStatus(self.COM_DeviceStatus(channel = channel))
    
    def temperature_stable(self, channel = 1):
        return MeCom_TemperatureStability(self.TEC_TemperatureIsStable(channel = channel))

    #
    #
    # inheritance functions
    #
    #


    def _send_and_receive(self, frame):
        raise NotImplementedError()

    
    def _send_and_ignore_receive(self, frame):
        raise NotImplementedError()
    