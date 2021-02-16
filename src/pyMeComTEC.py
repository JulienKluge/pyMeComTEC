from struct import pack, unpack

import pyMeComTEC_autogen
from pyMeComTEC_Helper import MeComError, MeComException, MeParFlags, MeParType, MeCom_DeviceStatus, MeCom_TemperatureIsStable

"""
Meerstetter TEC Abstract class.
This class forms and interprets queries send and received as byte arrays.

It can be put in any interface needed and is used by the implemented interfaces in this package.
"""
class TEC(pyMeComTEC_autogen._TEC_autogen):

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
    
    def _compose_bulkread_frame(self, mepar_ids, channels):
        if len(mepar_ids) !=  len(channels):
            raise Exception("Bulk read frame got unequal amount of mepar ids {}, and channels {}".format(len(mepar_ids), len(channels)))
        data_length = len(mepar_ids) * 3
        if (data_length > (232 - 0)):
            raise Exception("Too much data for a single frame was attempted to be sent")
        data_str = []
        for i in range(len(mepar_ids)):
            data_str += "{:04X}{:02X}".format(mepar_ids[i], channels[i])
        self._advance_sequence_number()
        frame = "#{}{:04X}?VX{:02X}{}".format(
            self.tec_address,
            self.sequence_number,
            len(mepar_ids),
            "".join(data_str)
        )
        return self._appendCRC(frame.encode())

    def _appendCRC(self, frame_str):
        return frame_str + self._form_crc(frame_str)

    def _form_crc(self, frame_str):
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
        return crc
    
    def _advance_sequence_number(self):
        self.sequence_number = self.sequence_number + 1
        if (self.sequence_number > 65535):
            self.sequence_number = 0
    
    def _validate_answer(self, answer, overwrite_checksum = ""):
        if (len(answer) < 11):
            raise Exception("Answer was not complete")
        body_arr = answer[:-4]
        test_crc = answer[-4:]
        error_indicator = body_arr[-3]
        if (error_indicator == 43): #i don't know either why indexing in a byte array gives me an int... 43==b'+'
            error_number = int(body_arr[-2:], 16)
            raise MeComException(error_number)

        if (not self.check_crc):
            return True
        if (overwrite_checksum == ""):
            calc_crc = self._form_crc(body_arr)
        else:
            calc_crc = overwrite_checksum
        if (test_crc != calc_crc):
            raise Exception("Mismatch in checksums")
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
    
    def _extract_bulkread_payload(self, answer, mepar_types):
        payload = answer[7:-4]
        read_position = 0
        read_index = 0
        read_values = []
        while read_position < len(payload) and read_index < len(mepar_types):
            current_type = mepar_types[read_index]
            read_offset = current_type.get_type_hex_length()
            read_value = payload[read_position:(read_position + read_offset)]
            read_values += [current_type.interpret_type(read_value)]
            read_position += read_offset
            read_index += 1
        if len(mepar_types) != len(read_values):
            raise Exception("Only {} read out of the requested {} reads were possible".format(len(read_values), len(mepar_types)))
        return read_values
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
    Reads the firmware identification string of the TEC.
    """
    def read_firmware_id(self):
        frame = self._compose_identification_frame()
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        id_str = self._extract_payload(answer)
        return (id_str.decode()).strip()


    """
    Reads the available metadata for a specified MeParID
    """
    def read_metadata(self, mepar_id, channel = 1):
        if (type(channel) == list):
            return [self.read_metadata(mepar_id, c) for c in channel]
        frame = self._compose_metadata_frame(mepar_id, channel)
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        return self._extract_metadata_payload(answer)
    

    """
    Reads the value of a specified MeParID and converts it to the specified type
    """
    def _read_value(self, mepar_id, mepar_type, channel):
        if (type(channel) == list):
            return [self._read_value(mepar_id, mepar_type, c) for c in channel]
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
        if (type(channel) == list):
            return [self.read_big_value(mepar_id, mepar_type, c, read_start = read_start, max_nr_read = max_nr_read) for c in channel]
        frame = self._compose_bigread_frame(mepar_id, channel, read_start, max_nr_read)
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        payload = self._extract_bigdata_payload(answer, mepar_type)
        return payload #TODO parse further
    
    """
    Reads the raw response for a given MeParID
    """
    def read_raw(self, mepar_id, channel = 1):
        if (type(channel) == list):
            return [self.read_raw(mepar_id, c) for c in channel]
        frame = self._compose_read_frame(mepar_id, channel)
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        payload = self._extract_payload(answer)
        return payload

    """
    """
    def read_bulk(self, mepar_ids, channels = 1):
        if (type(mepar_ids) != list and type(channels) != list):
            mepar_ids = [mepar_ids]
            channels = [channels]
        if (type(mepar_ids) != list):
            mepar_ids = [mepar_ids for _ in range(len(channels))]
        if (type(channels) != list):
            channels = [channels for _ in range(len(mepar_ids))]
        if (len(mepar_ids) != len(channels)):
            raise Exception("The number of requested mepar id's {} should be equal to the number of the respective requested channels {}".format(
                len(mepar_ids),
                len(channels)
            ))
        mepar_arr = []
        for m_id, c in zip(mepar_ids, channels):
            t_param = self.find_meparid(m_id)
            if t_param == None:
                raise Exception("MeparId \"{}\" could not be found as a valid parameter".format(m_id))
            t_id = t_param["id"]
            t_type = t_param["mepar_type"]
            mepar_arr += [[t_id, t_type, c]]
        
        frame = self._compose_bulkread_frame(
            [p_id for p_id, _, _ in mepar_arr],
            [p_c for _, _, p_c in mepar_arr]
        )
        answer = self._send_and_receive(frame)
        self._validate_answer(answer)
        payload = self._extract_bulkread_payload(answer, [p_t for _, p_t, _ in mepar_arr])
        return payload
        

    """
    Writes the given value to a specified MeParID
    """
    def _write_value(self, mepar_id, mepar_type, raw_value, channel, fire_and_forget = False):
        if (type(channel) == list):
            return [self._write_value(mepar_id, mepar_type, raw_value, c, fire_and_forget = fire_and_forget) for c in channel]
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
    def write_big_value(self, mepar_id, mepar_type, raw_value, channel, read_start = 0, fire_and_forget = False):
        if (type(channel) == list):
            return [self.write_big_value(mepar_id, mepar_type, raw_value, c, read_start = read_start, fire_and_forget = fire_and_forget) for c in channel]
        frame = self._compose_bigset_frame(mepar_id, mepar_type, channel, raw_value, read_start)
        if (fire_and_forget or self.tec_address == 255):
            self._send_and_ignore_receive(frame)
            return True
        else:
            answer = self._send_and_receive(frame)
            self._validate_answer(answer, overwrite_checksum = frame[-4:])
            payload = self._extract_payload(answer)
            return payload == b''

    """
    Writes a raw packet into a frame and sends it to the TEC
    """
    def write_raw(self, mepar_id, value, channel = 1, fire_and_forget = False):
        if (type(channel) == list):
            return [self.write_raw(mepar_id, value, c, fire_and_forget = fire_and_forget) for c in channel]
        frame = self._compose_set_frame(mepar_id, channel, value)
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

    #temp
    def temperature(self, channel = 1):
        return self.Get_TEC_ObjectTemperature(channel = channel)

    def nominal_temperature(self, channel = 1):
        return self.Get_TEC_RampNominalObjectTemperature(channel = channel)

    def target_temperature(self, channel = 1):
        return self.Get_TEC_TargetObjectTemp(channel = channel)
    def write_target_temperature(self, value, channel = 1):
        return self.Set_TEC_TargetObjectTemp(value, channel = channel, fire_and_forget = False)


    #current
    def current(self, channel = 1):
        return self.Get_TEC_ActualOutputCurrent(channel = channel)
    
    def current_limit(self, channel = 1):
        return self.Get_TEC_CurrentLimitation(channel = channel)
    def write_current_limit(self, limit, channel = 1, fire_and_forget = False):
        return self.Set_TEC_CurrentLimitation(channel = channel, value = limit, fire_and_forget = fire_and_forget)

    def current_error_threshold(self, channel = 1):
        return self.Get_TEC_CurrentErrorThreshold(channel = channel)
    def write_current_error_threshold(self, threshold, channel = 1, fire_and_forget = False):
        return self.Set_TEC_CurrentErrorThreshold(channel = channel, value = threshold, fire_and_forget = fire_and_forget)
        

    #voltage
    def voltage(self, channel = 1):
        return self.Get_TEC_ActualOutputVoltage(channel = channel)
    
    def voltage_limit(self, channel = 1):
        return self.Get_TEC_VoltageLimitation(channel = channel)
    def write_voltage_limit(self, limit, channel = 1, fire_and_forget = False):
        return self.Set_TEC_VoltageLimitation(channel = channel, value = limit, fire_and_forget = fire_and_forget)

    def voltage_error_threshold(self, channel = 1):
        return self.Get_TEC_VoltageErrorThreshold(channel = channel)
    def write_voltage_error_threshold(self, threshold, channel = 1, fire_and_forget = False):
        return self.Set_TEC_VoltageErrorThreshold(channel = channel, value = threshold, fire_and_forget = fire_and_forget)
    
    
    #misc
    def get_error(self, channel = 1):
        if (type(channel) == list):
            return [self.get_error(channel = c) for c in channel]
        error_num = self.Get_COM_ErrorNumber(channel = channel)
        error_inst = self.Get_COM_ErrorInstance(channel = channel)
        error_param = self.Get_COM_ErrorParameter(channel = channel)
        if error_num in self.TEC_ERRORS:
            err_description = self.TEC_ERRORS[error_num]
        else:
            err_description = "UNKNOWN ERROR"
        return (error_num, error_inst, error_param, err_description)

    def status(self, channel = 1):
        status_returns = self.Get_COM_DeviceStatus(channel = channel)
        if (type(status_returns) == list):
            return [MeCom_DeviceStatus(s) for s in status_returns]
        else:
            return MeCom_DeviceStatus(status_returns)
    
    def temperature_is_stable(self, channel = 1):
        stability_returns = self.Get_TEC_TemperatureIsStable(channel = channel)
        if (type(stability_returns) == list):
            return [MeCom_TemperatureIsStable(s)  == MeCom_TemperatureIsStable.Stable for s in stability_returns]
        else:
            return MeCom_TemperatureIsStable(stability_returns) == MeCom_TemperatureIsStable.Stable

    #
    #
    # inheritance functions
    #
    #


    def _send_and_receive(self, frame):
        raise NotImplementedError()

    
    def _send_and_ignore_receive(self, frame):
        raise NotImplementedError()
