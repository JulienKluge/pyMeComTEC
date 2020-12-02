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
    # Parameter dictionary
    #
    #
    TEC_PARAMETERS = [
        {"prefix": "COM", "id": 100, "name": "DeviceType", "type": int, "readonly": True},
        {"prefix": "COM", "id": 101, "name": "HardwareVersion", "type": int, "readonly": True},
        {"prefix": "COM", "id": 102, "name": "SerialNumber", "type": int, "readonly": True},
        {"prefix": "COM", "id": 103, "name": "FirmwareVersion", "type": int, "readonly": True},
        {"prefix": "COM", "id": 104, "name": "DeviceStatus", "type": int, "readonly": True},
        {"prefix": "COM", "id": 105, "name": "ErrorNumber", "type": int, "readonly": True},
        {"prefix": "COM", "id": 106, "name": "ErrorInstance", "type": int, "readonly": True},
        {"prefix": "COM", "id": 107, "name": "ErrorParameter", "type": int, "readonly": True},
        {"prefix": "COM", "id": 108, "name": "ParameterSystemFlashSaveOff", "type": int, "readonly": False},
        {"prefix": "COM", "id": 109, "name": "ParameterSystemFlashStatus", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1000, "name": "ObjectTemperature", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1001, "name": "SinkTemperature", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1010, "name": "TargetObjectTemperature", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1011, "name": "RampNominalObjectTemperature", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1012, "name": "ThermalPowerModelCurrent", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1020, "name": "ActualOutputCurrent", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1021, "name": "ActualOutputVoltage", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1030, "name": "PIDLowerLimitation", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1031, "name": "PIDUpperLimitation", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1032, "name": "PIDControlVariable", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1040, "name": "ObjectSensorRawADCValue", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1041, "name": "SinkSensorRawADCValue", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1042, "name": "ObjectSensorResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1043, "name": "SinkSensorResitance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1044, "name": "SinkSensorTemperature", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1050, "name": "FirmwareVersion", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1051, "name": "FirmwareBuildNumber", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1052, "name": "HardwareVersion", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1053, "name": "SerialNumber", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1060, "name": "DriverInputVoltage", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1061, "name": "MedVInternalSupply", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1062, "name": "3VInternalSupply", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1063, "name": "BasePlateTemperature", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1070, "name": "ErrorNumber", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1071, "name": "ErrorInstance", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1072, "name": "ErrorParameter", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1090, "name": "ParallelActualOutputCurrent", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1080, "name": "DriverStatus", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1081, "name": "ParameterSystemFlashStatus", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 1100, "name": "FanRelativeCoolingPower", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1101, "name": "FanNominalFanSpeed", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1102, "name": "FanActualFanSpeed", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1103, "name": "FanActualPwmLevel", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 1200, "name": "TemperatureIsStable", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 2000, "name": "OutputStageInputSelection", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 2010, "name": "OutputStageEnable", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 2020, "name": "SetStaticCurrent", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 2021, "name": "SetStaticVoltage", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 2030, "name": "CurrentLimitation", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 2031, "name": "VoltageLimitation", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 2032, "name": "CurrentErrorThreshold", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 2033, "name": "VoltageErrorThreshold", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 2040, "name": "GeneralOperatingMode", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 2051, "name": "DeviceAddress", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 2050, "name": "RS485CH1BaudRate", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 2052, "name": "RS485CH1ResponseDelay", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 2060, "name": "ComWatchDogTimeout", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3000, "name": "TargetObjectTemp", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3003, "name": "CoarseTempRamp", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3002, "name": "ProximityWidth", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3010, "name": "Kp", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3011, "name": "Ti", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3012, "name": "Td", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3013, "name": "DPartDampPT1", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3020, "name": "ModelizationMode", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 3030, "name": "PeltierMaxCurrent", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3031, "name": "PeltierMaxVoltage", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3032, "name": "PeltierCoolingCapacity", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3033, "name": "PeltierDeltaTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3034, "name": "PeltierPositiveCurrentIs", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 3040, "name": "ResistorResistance", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 3041, "name": "ResistorMaxCurrent", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4001, "name": "TemperatureOffset", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4002, "name": "TemperatureGain", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4010, "name": "LowerErrorThreshold", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4011, "name": "UpperErrorThreshold", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4012, "name": "MaxTempChange", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4020, "name": "NTCLowerPointTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4021, "name": "NTCLowerPointResistance", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4022, "name": "NTCMiddlePointTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4023, "name": "NTCMiddlePointResistance", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4024, "name": "NTCUpperPointTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4025, "name": "NTCUpperPointResistance", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4040, "name": "StabilityTemperatureWindow", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4041, "name": "StabilityMinTimeInWindow", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4042, "name": "StabilityMaxStabiTime", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 4030, "name": "MeasLowestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 4031, "name": "MeasHighestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 4032, "name": "MeasTempAtLowestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 4033, "name": "MeasTempAtHighestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 5001, "name": "TemperatureOffset", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5002, "name": "TemperatureGain", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5010, "name": "LowerErrorThreshold", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5011, "name": "UpperErrorThreshold", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5012, "name": "MaxTempChange", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5020, "name": "NTCLowerPointTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5021, "name": "NTCLowerPointResistance", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5022, "name": "NTCMiddlePointTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5023, "name": "NTCMiddlePointResistance", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5024, "name": "NTCUpperPointTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5025, "name": "NTCUpperPointResistance", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5030, "name": "SinkTemperatureSelection", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 5031, "name": "FixedTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 5040, "name": "MeasLowestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 5041, "name": "MeasHighestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 5042, "name": "MeasTempAtLowestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 5043, "name": "MeasTempAtHighestResistance", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 6000, "name": "ObjMeasPGAGain", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6001, "name": "ObjMeasCurrentSource", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6002, "name": "ObjMeasADCRs", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6003, "name": "ObjMeasADCCalibOffset", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6004, "name": "ObjMeasADCCalibGain", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6005, "name": "ObjMeasSensorTypeSelection", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6010, "name": "SinMeasADCRv", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6013, "name": "SinMeasADCVps", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6011, "name": "SinMeasADCCalibOffset", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6012, "name": "SinMeasADCCalibGain", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6020, "name": "DisplayType", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6021, "name": "DisplayLineDefText", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6022, "name": "DisplayLineAltText", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6023, "name": "DisplayLineAltMode", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6100, "name": "PbcFunction", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6110, "name": "ChangeButtonLowTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6111, "name": "ChangeButtonHighTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6112, "name": "ChangeButtonStepSize", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6200, "name": "FanControlEnable", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6210, "name": "FanActualTempSource", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6211, "name": "FanTargetTemp", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6212, "name": "FanTempKp", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6213, "name": "FanTempTi", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6214, "name": "FanTempTd", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6220, "name": "FanSpeedMin", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6221, "name": "FanSpeedMax", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6222, "name": "FanSpeedKp", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6223, "name": "FanSpeedTi", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6224, "name": "FanSpeedTd", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 6225, "name": "FanSpeedBypass", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6230, "name": "PwmFrequency", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6300, "name": "MiscActObjectTempSource", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6310, "name": "MiscDelayTillReset", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 6320, "name": "MiscError108Delay", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 50000, "name": "LiveEnable", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 50001, "name": "LiveSetCurrent", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 50002, "name": "LiveSetVoltage", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 50010, "name": "SineRampStartPoint", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 50011, "name": "ObjectTargetTempSourceSelection", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 50012, "name": "ObjectTargetTemperature", "type": float, "readonly": False},
        {"prefix": "TEC", "id": 51000, "name": "AtmAutoTuningStart", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 51001, "name": "AtmAutoTuningCancel", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 51002, "name": "AtmThermalModelSpeed", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 51010, "name": "AtmTuningParameter2A", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51011, "name": "AtmTuningParameter2D", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51012, "name": "AtmTuningParameterKu", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51013, "name": "AtmTuningParameterTu", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51014, "name": "AtmPIDParameterKp", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51015, "name": "AtmPIDParameterTi", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51016, "name": "AtmPIDParameterTd", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51022, "name": "AtmSlowPIParameterKp", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51023, "name": "AtmSlowPIParameterTi", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51024, "name": "AtmPIDDPartDamping", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51017, "name": "AtmCoarseTempRamp", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51018, "name": "AtmProximityWidth", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 51020, "name": "AtmTuningStatus", "type": int, "readonly": True},
        {"prefix": "TEC", "id": 51021, "name": "AtmTuningProgress", "type": float, "readonly": True},
        {"prefix": "TEC", "id": 52000, "name": "LutTableStart", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52001, "name": "LutTableStop", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52002, "name": "LutTableStatus", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52003, "name": "LutCurrentTableLine", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52010, "name": "LutTableIDSelection", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52012, "name": "LutNrOfRepetitions", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52100, "name": "PbcEnableFunction", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52101, "name": "PbcSetOutputToPushPull", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52102, "name": "PbcSetOutputStates", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52103, "name": "PbcReadInputStates", "type": int, "readonly": False},
        {"prefix": "TEC", "id": 52200, "name": "ExternalActualObjectTemperature", "type": float, "readonly": False}
    ]
    def find_parameter_by_name(self, name):
        pass
    

    #
    #
    # inheritance functions
    #
    #


    def _sendAndReceive(self, byteArr):
        raise NotImplementedError()
    

    #
    #
    # auto generated function
    #
    #

    #so, in principle, we could be cool here, use __getattr__ for catching unknown method names,
    #match this against our param list, and call the appropriate method.
    #however, we'd loose intellisense then and I'd rather have that. So I choose to auto generate
    #the method list instead

