#this test script has to be started in its own directory with the whole repository downloaded
import sys
sys.path.insert(0, '../../src')

from pyMeComTEC_Serial import TEC_Serial
from pyMeComTEC_Helper import (
        MeParType,
        MeCom_DeviceStatus,
        MeCom_SaveDataToFlash,
        MeCom_DriverStatus,
        MeCom_FlashStatus,
        MeCom_TemperatureIsStable,
        MeCom_InputSelection,
        MeCom_OutputStageStatus,
        MeCom_GeneralOperatingMode,
        MeCom_ThermalPowerRegulationMode,
        MeCom_PositiveCurrentIs,
        MeCom_SensorType,
        MeCom_SinkTemperatureSelection,
        MeCom_TuningStatus,
        MeCom_PGAGain,
        #MeCom_CurrentSource_1092,
        MeCom_CurrentSource_Other,
        #MeCom_CurrentSource2Out_1092,
        MeCom_CurrentSource2Out_Other,
        MeCom_MeasurementType,
        MeCom_SensorTypeSelection,
        MeCom_LookupTableStatus,
        MeCom_DisplayType,
        MeCom_DisplayLineAlternativeMode,
        MeCom_GPIOFunction,
        MeCom_GPIOLevelAssignment,
        MeCom_HardwareConfiguration,
        MeCom_GPIOChannel,
        MeCom_ActualTemperatureSource,
        MeCom_ObserveMode,
        MeCom_ControlSpeed,
        MeCom_SourceSelection,
        MeCom_DeviceTemperatureMode
    )
import time


def main():
    #allocate the tec object for a serial communication at serial port COM10
    tec = TEC_Serial(port = "COM10")

    #
    # For some values, automatic enumerations are available

    #
    # ATTENTION HERE: FOR THE TEC 1092, THE MeCom_CurrentSource AND MeCom_CurrentSource2Out
    # ARE DIFFERENT TO ALL OTHER TECS
    # THESE ARE CURRENTLY COMMENTED OUT. USE WITH CAUTION
    # THE DIFFERENCE WAS MADE INTO THE NAME:
    # MeCom_CurrentSource_1092 vs. MeCom_CurrentSource_Other
    # AND
    # MeCom_CurrentSource2Out_1092 vs. MeCom_CurrentSource2Out_Other
    #
    triples = [
        [MeCom_DeviceStatus, tec.Get_COM_DeviceStatus, 104],
        [MeCom_SaveDataToFlash, tec.Get_COM_ParameterSystemFlashStatus, 109],
        [MeCom_DriverStatus, tec.Get_TEC_DriverStatus, 1080],
        [MeCom_FlashStatus, tec.Get_TEC_ParameterSystemFlashStatus, 1081],
        [MeCom_TemperatureIsStable, tec.Get_TEC_TemperatureIsStable, 1200],
        [MeCom_InputSelection, tec.Get_TEC_OutputStageInputSelection, 2000],
        [MeCom_OutputStageStatus, tec.Get_TEC_OutputStageEnable, 2010],
        [MeCom_GeneralOperatingMode, tec.Get_TEC_GeneralOperatingMode, 2040],
        [MeCom_ThermalPowerRegulationMode, tec.Get_TEC_ModelizationMode, 3020],
        [MeCom_PositiveCurrentIs, tec.Get_TEC_PeltierPositiveCurrentIs, 3034],
        [MeCom_SensorType, 4034, 4034],
        [MeCom_SinkTemperatureSelection, tec.Get_TEC_SinkTemperatureSelection, 5030],
        [MeCom_TuningStatus, tec.Get_TEC_AtmTuningStatus, 51020],
        [MeCom_PGAGain, tec.Get_TEC_ObjMeasPGAGain, 6000],
        #[MeCom_CurrentSource_1092, tec.Get_TEC_ObjMeasCurrentSource, 6001],
        [MeCom_CurrentSource_Other, tec.Get_TEC_ObjMeasCurrentSource, 6001],
        #[MeCom_CurrentSource2Out_1092, 6008, 6008],
        [MeCom_CurrentSource2Out_Other, 6008, 6008],
        [MeCom_MeasurementType, 6009, 6009],
        [MeCom_SensorTypeSelection, tec.Get_TEC_ObjMeasSensorTypeSelection, 6005],
        [MeCom_LookupTableStatus, tec.Get_TEC_LutTableStatus, 52002],
        [MeCom_DisplayType, tec.Get_TEC_DisplayType, 6020],
        [MeCom_DisplayLineAlternativeMode, tec.Get_TEC_AlternativeMode, 6023],
        [MeCom_GPIOFunction, tec.Get_TEC_PbcFunction, 6100],
        [MeCom_GPIOLevelAssignment, 6101, 6101],
        [MeCom_HardwareConfiguration, 6102, 6102],
        [MeCom_GPIOChannel, 6103, 6103],
        [MeCom_ActualTemperatureSource, 6120, 6120],
        [MeCom_ObserveMode, 6302, 6302],
        [MeCom_ControlSpeed, 6301, 6301],
        [MeCom_SourceSelection, tec.Get_TEC_MiscActObjectTempSource, 6300],
        [MeCom_DeviceTemperatureMode, 6330, 6330]
    ]

    #traverse all:
    for enumType, function, meparid in triples:
        if type(function) == int:
            result = tec._read_value(meparid, MeParType.INT32)
        else:
            result = function()
        enum = enumType(result)
        print("{:<32} (MeParID: {:<5}): Value {} = \"{:<21}\" [{}]".format(
            enumType.__name__,
            meparid,
            enum,
            enum.name,
            "no associated function" if type(function) == int else function.__name__
            )
        )
    


if __name__ == '__main__':
    main()

#
# EXAMPLE OUTPUT
#
#MeCom_DeviceStatus               (MeParID: 104  ): Value 2 = "Run                  " [Get_COM_DeviceStatus]
#MeCom_SaveDataToFlash            (MeParID: 109  ): Value 0 = "AllParameters        " [Get_COM_ParameterSystemFlashStatus]
#MeCom_DriverStatus               (MeParID: 1080 ): Value 2 = "Run                  " [Get_TEC_DriverStatus]
#MeCom_FlashStatus                (MeParID: 1081 ): Value 0 = "AllParameters        " [Get_TEC_ParameterSystemFlashStatus]
#MeCom_TemperatureIsStable        (MeParID: 1200 ): Value 2 = "Stable               " [Get_TEC_TemperatureIsStable]
#MeCom_InputSelection             (MeParID: 2000 ): Value 2 = "TemperatureController" [Get_TEC_OutputStageInputSelection]
#MeCom_OutputStageStatus          (MeParID: 2010 ): Value 1 = "StaticOn             " [Get_TEC_OutputStageEnable]
#MeCom_GeneralOperatingMode       (MeParID: 2040 ): Value 0 = "Single               " [Get_TEC_GeneralOperatingMode]
#MeCom_ThermalPowerRegulationMode (MeParID: 3020 ): Value 0 = "PeltierFullControl   " [Get_TEC_ModelizationMode]
#MeCom_PositiveCurrentIs          (MeParID: 3034 ): Value 1 = "Heating              " [Get_TEC_PeltierPositiveCurrentIs]
#MeCom_SensorType                 (MeParID: 4034 ): Value 5 = "NTC56K               " [no associated function]
#MeCom_SinkTemperatureSelection   (MeParID: 5030 ): Value 1 = "FixedValue           " [Get_TEC_SinkTemperatureSelection]
#MeCom_TuningStatus               (MeParID: 51020): Value 0 = "Idle                 " [Get_TEC_AtmTuningStatus]
#MeCom_PGAGain                    (MeParID: 6000 ): Value 9 = "AutoGain1_8_32       " [Get_TEC_ObjMeasPGAGain]
#MeCom_CurrentSource_Other        (MeParID: 6001 ): Value 1 = "uA50                 " [Get_TEC_ObjMeasCurrentSource]
#MeCom_CurrentSource2Out_Other    (MeParID: 6008 ): Value 0 = "OFF                  " [no associated function]
#MeCom_MeasurementType            (MeParID: 6009 ): Value 0 = "Resistance           " [no associated function]
#MeCom_SensorTypeSelection        (MeParID: 6005 ): Value 0 = "NTC                  " [Get_TEC_ObjMeasSensorTypeSelection]
#MeCom_LookupTableStatus          (MeParID: 52002): Value 1 = "TableDataNotvalid    " [Get_TEC_LutTableStatus]
#MeCom_DisplayType                (MeParID: 6020 ): Value 1 = "OLED2x16             " [Get_TEC_DisplayType]
#MeCom_DisplayLineAlternativeMode (MeParID: 6023 ): Value 0 = "NoneMode             " [Get_TEC_AlternativeMode]
#MeCom_GPIOFunction               (MeParID: 6100 ): Value 0 = "NoFunction           " [Get_TEC_PbcFunction]
#MeCom_GPIOLevelAssignment        (MeParID: 6101 ): Value 0 = "Positive             " [no associated function]
#MeCom_HardwareConfiguration      (MeParID: 6102 ): Value 0 = "INWeakNo             " [no associated function]
#MeCom_GPIOChannel                (MeParID: 6103 ): Value 1 = "Channel1             " [no associated function]
#MeCom_ActualTemperatureSource    (MeParID: 6120 ): Value 0 = "CH1Sink              " [no associated function]
#MeCom_ObserveMode                (MeParID: 6302 ): Value 0 = "Automatic            " [no associated function]
#MeCom_ControlSpeed               (MeParID: 6301 ): Value 0 = "Hz_10                " [no associated function]
#MeCom_SourceSelection            (MeParID: 6300 ): Value 0 = "InternalOwnChannel   " [Get_TEC_MiscActObjectTempSource]
#MeCom_DeviceTemperatureMode      (MeParID: 6330 ): Value 0 = "Standard             " [no associated function]
#
