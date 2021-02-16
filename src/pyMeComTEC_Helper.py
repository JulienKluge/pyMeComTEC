from enum import Enum
from struct import pack, unpack


class MeComError(Enum):
    EER_CMD_NOT_AVAILABLE = 1 #Command not available
    EER_DEVICE_BUSY = 2 #Device is busy
    ERR_GENERAL_COM = 3 #General communication error
    EER_FORMAT = 4 #Format error
    EER_PAR_NOT_AVAILABLE = 5 #Parameter is not available
    EER_PAR_NOT_WRITABLE = 6 #Parameter is read only
    EER_PAR_OUT_OF_RANGE = 7 #Value is out of range
    EER_PAR_INST_NOT_AVAILABLE = 8 #Instance is not available
    ERR_PAR_GENERAL_FAILURE = 9 #Parameter general Error. Device internal failure on this parameter.

    ERR_CUSTOM_EMERGENCY_STOP = 11 # Emergency Stop

    ERR_DEVICE_SPECIFIC = -1 # device specific

    def get_message(self):
        if (self == MeComError.EER_CMD_NOT_AVAILABLE):
            return "Command not available"
        elif (self == MeComError.EER_DEVICE_BUSY):
            return "Device is busy"
        elif (self == MeComError.ERR_GENERAL_COM):
            return "General communication error"
        elif (self == MeComError.EER_FORMAT):
            return "Format error"
        elif (self == MeComError.EER_PAR_NOT_AVAILABLE):
            return "Parameter is not available"
        elif (self == MeComError.EER_PAR_NOT_WRITABLE):
            return "Parameter is read only"
        elif (self == MeComError.EER_PAR_OUT_OF_RANGE):
            return "Value is out of range"
        elif (self == MeComError.EER_PAR_INST_NOT_AVAILABLE):
            return "Instance is not available"
        elif (self == MeComError.ERR_PAR_GENERAL_FAILURE):
            return "Parameter general Error. Device internal failure on this parameter."
        elif (self == MeComError.ERR_CUSTOM_EMERGENCY_STOP):
            return "Emergency Stop was sent."
        else:
            return "Device specific error"

    @staticmethod
    def parse_error_number(num):
        if (1 <= num and 9 >= num):
            return MeComError(num)
        else:
            MeComError.ERR_DEVICE_SPECIFIC

class MeComException(Exception):
    def __init__(self, error_number):
        self.mecom_error_number = error_number
        self.mecom_error = MeComError.parse_error_number(error_number)

        super().__init__(self.mecom_error.get_message())

class MeParFlags():
    def __init__(self, flags):
        self.Read = bool(flags & 0x1)
        self.Write = bool((flags >> 1) & 0x1)
        self.Unused_2 = bool((flags >> 2) & 0x1)
        self.Unused_3 = bool((flags >> 3) & 0x1)
        self.Unused_4 = bool((flags >> 4) & 0x1)
        self.Unused_5 = bool((flags >> 5) & 0x1)
        self.Unused_6 = bool((flags >> 6) & 0x1)
        self.Unused_7 = bool((flags >> 7) & 0x1)

    def is_readonly(self):
        return (not self.Write) and self.Read
    def is_writeonly(self):
        return (not self.Read) and self.Write
    def is_readwrite(self):
        return self.Read and self.Write
    

class MeParType(Enum):
    FLOAT32 = 0
    INT32 = 1
    DOUBLE64 = 2 #not currently used
    LATIN1 = 3
    BYTE = 4

    def interpret_type(self, arg):
        if (type(arg) == bytes):
            arg = arg.decode()
        if (self == MeParType.FLOAT32):
            return unpack('!f', bytes.fromhex(arg))[0]
        elif (self == MeParType.INT32):
            return int(arg, 16)
        elif (self == self.DOUBLE64):
            return unpack('d', bytes.fromhex(arg))[0]
        elif (self == self.LATIN1):
            return arg
        elif (self == self.BYTE):
            return bytes.fromhex(arg)

    def from_type(self, arg):
        if (self == MeParType.FLOAT32):
            return "{:08X}".format(unpack('<I', pack('<f', arg))[0]) #year, the author was right, don't ask
        elif (self == MeParType.INT32):
            return "{:08X}".format(arg)
        elif (self == self.DOUBLE64): #not implemented yet, but we plan for the future, don't we?!
            return "{:016X}".format(unpack('<Q', pack('<d', arg))[0]) #noopeee
        elif (self == self.LATIN1):
            return arg
        elif (self == self.BYTE):
            return arg.decode()
    
    def get_type_hex_length(self):
        if (self == MeParType.FLOAT32):
            return 8
        elif (self == MeParType.INT32):
            return 8
        elif (self == self.DOUBLE64):
            return 16
        elif (self == self.LATIN1):
            return 2
        elif (self == self.BYTE):
            return 2
    
    def _finish_bigdata_array(self, arr):
        if (self == MeParType.LATIN1):
            return "".join(arr[:-1])
        else:
            return arr
    
    def get_type(self):
        if (self == MeParType.FLOAT32):
            return float
        elif (self == MeParType.INT32):
            return int
        elif (self == MeParType.DOUBLE64):
            return float
        elif (self == MeParType.LATIN1):
            return str
        elif (self == MeParType.BYTE):
            return bytes

class MeCom_DeviceStatus(Enum): #104
    Init = 0
    Ready = 1
    Run = 2
    Error = 3
    Bootloader = 4
    DeviceWillReset = 5

class MeCom_SaveDataToFlash(Enum): #109
    AllParameters = 0
    SavePending = 1
    Disabled = 2

class MeCom_DriverStatus(Enum): #1080
    Init = 0
    Ready = 1
    Run = 2
    Error = 3
    Bootloader = 4
    DeviceWillReset = 5

class MeCom_FlashStatus(Enum): #1081
    AllParameters = 0
    Pending = 1

class MeCom_TemperatureIsStable(Enum): #1200
    RegulationNotActive = 0
    NotStable = 1
    Stable = 2

class MeCom_InputSelection(Enum): #2000
    StaticCurrentVoltage = 0
    LiveCurrentVoltage = 1
    TemperatureController = 2

class MeCom_OutputStageStatus(Enum): #2010
    StaticOff = 0
    StaticOn = 1
    LiveOffOn = 2
    HWEnable = 3

class MeCom_GeneralOperatingMode(Enum): #2040
    Single = 0
    Parallel_IndividualLoads = 1
    Parallel_CommonLoad = 2

class MeCom_ThermalPowerRegulationMode(Enum): #3020
    PeltierFullControl = 0
    PeltierHeatCoolOnly = 1
    ResistorHeatOnly = 2

class MeCom_PositiveCurrentIs(Enum): #3034
    Cooling = 0
    Heating = 1

class MeCom_SensorType(Enum): #4034
    Unknown = 0
    Pt100 = 1
    Pt1000 = 2
    NTC18K = 3
    NTC39K = 4
    NTC56K = 5
    NTC1M = 6
    VIN1 = 7

class MeCom_SinkTemperatureSelection(Enum): #5030
    External = 0
    FixedValue = 1

class MeCom_TuningStatus(Enum): #51020
    Idle = 0
    RampingToTargetTemperature = 1
    PreparingForAcquisition = 2
    AcquiringData = 3
    Success = 4
    Error = 10

class MeCom_PGAGain(Enum): #6000
    Gain1 = 0
    Gain2 = 1
    Gain4 = 2
    Gain8 = 3
    Gain16 = 4
    Gain32 = 5
    Gain64 = 6
    Gain128 = 7
    AutoGain1_8 = 8
    AutoGain1_8_32 = 9

#Really? Separating this for multiple models? Uff..
class MeCom_CurrentSource_1092(Enum): #6001 - TEC-1092
    OFF = 0
    uA10 = 1
    uA50 = 2
    uA100 = 3
    uA250 = 4
    uA500 = 5
    uA1000 = 6
    uA1500 = 7
class MeCom_CurrentSource_Other(Enum): #6001 - Other TECs
    OFF = 0
    uA50 = 1
    uA100 = 2
    uA250 = 3
    uA500 = 4
    uA750 = 5
    uA1000 = 6
    uA1500 = 7

class MeCom_CurrentSource2Out_1092(Enum): #6008 - TEC-1092
    OFF = 0
    AIN0_UB = 1
    AIN1_UA = 2
    AIN2 = 3
    AIN3_IA = 4
    REFP0_IB = 5
    REFN0 = 6
class MeCom_CurrentSource2Out_Other(Enum): #6008 - Other TECs
    OFF = 0
    AIN0_UB = 1
    AIN1_UA = 2
    AIN2_IA = 3
    AIN3 = 4

class MeCom_MeasurementType(Enum): #6009
    Resistance = 0
    Voltage = 1

class MeCom_SensorTypeSelection(Enum): #6005
    NTC = 0
    Pt100 = 1
    Pt1000 = 2
    Voltage = 3

class MeCom_LookupTableStatus(Enum): #52002
    NotInitialized = 0
    TableDataNotvalid = 1
    AnalyzingDataTable = 2
    Ready = 3
    Executing = 4
    MaxNumberOfTablesExceeded = 5
    SubTableNotFound = 6

class MeCom_DisplayType(Enum): #6020
    Off = 0
    OLED2x16 = 1

class MeCom_DisplayLineAlternativeMode(Enum): #6023
    NoneMode = 0
    OnError = 1
    ToggleOnError = 2
    Toggle = 3

class MeCom_GPIOFunction(Enum): #6100
    NoFunction = 0
    DataInterface = 1
    TEC_OK = 2
    Stable = 3
    HWEnable = 4
    FanPWM = 5
    FanTacho = 6
    Rmp_Stable = 7
    Run = 8
    TempUp = 9
    TempDown = 10
    Pump = 11
    LookupStart = 12
    Adr1 = 13
    Adr2 = 14
    Adr4 = 15
    FanStop = 16
    AltTargetT1 = 17
    AltTargetT2 = 18
    PowerSt0A = 19
    EncoderA = 20
    EncoderB = 21

class MeCom_GPIOLevelAssignment(Enum): #6101
    Positive = 0
    Negative = 1

class MeCom_HardwareConfiguration(Enum): #6102
    INWeakNo = 0
    INWeakUp = 1
    INWeakDown = 2
    OUTPushPull = 3
    OUTODNoPull = 4
    OUTODWeakUp = 5

class MeCom_GPIOChannel(Enum): #6103
    Channel1 = 1
    Channel2 = 2

class MeCom_ActualTemperatureSource(Enum): #6120
    CH1Sink = 0
    CH1Object = 1
    CH2Sink = 2
    CH2Object = 3
    DeviceTemperature = 4

class MeCom_ObserveMode(Enum): #6302
    Automatic = 0
    Disabled = 1
    Enabled = 2

class MeCom_ControlSpeed(Enum): #6301
    Hz_10 = 0
    Hz_80_90 = 1
    Hz_1 = 2

class MeCom_SourceSelection(Enum): #6300
    InternalOwnChannel = 0
    External_52200 = 1
    InternalChannel2 = 2

class MeCom_DeviceTemperatureMode(Enum): #6330
    Standard = 0
    Extended = 1

