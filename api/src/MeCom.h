#ifndef MECOM_H
#define MECOM_H

#include <stdint.h>

typedef enum 
{
    MeGet,
    MeSet,
    MeGetLimits,
} MeParCmd;

typedef struct
{
    int32_t Value;
    int32_t Min;
    int32_t Max;
} MeParLongFields;

typedef struct
{
    float Value;
    float Min;
    float Max;
} MeParFloatFields;

extern uint8_t MeCom_ResetDevice(uint8_t Address);
extern uint8_t MeCom_GetIdentString(uint8_t Address, int8_t *arr);
extern uint8_t MeCom_ParValuel(uint8_t Address, uint16_t ParId, uint8_t Inst, MeParLongFields  *Fields, MeParCmd Cmd);
extern uint8_t MeCom_ParValuef(uint8_t Address, uint16_t ParId, uint8_t Inst, MeParFloatFields *Fields, MeParCmd Cmd);


//**************************************************************************
//**********Definition of all Common Parameter Numbers**********************
//**************************************************************************

#define MeCom_COM_DeviceType(Address, Fields, Cmd)                      MeCom_ParValuel(Address, 100, 1, Fields, Cmd)
#define MeCom_COM_HardwareVersion(Address, Fields, Cmd)                 MeCom_ParValuel(Address, 101, 1, Fields, Cmd)
#define MeCom_COM_SerialNumber(Address, Fields, Cmd)                    MeCom_ParValuel(Address, 102, 1, Fields, Cmd)
#define MeCom_COM_FirmwareVersion(Address, Fields, Cmd)                 MeCom_ParValuel(Address, 103, 1, Fields, Cmd)
#define MeCom_COM_DeviceStatus(Address, Fields, Cmd)                    MeCom_ParValuel(Address, 104, 1, Fields, Cmd)
#define MeCom_COM_ErrorNumber(Address, Fields, Cmd)                     MeCom_ParValuel(Address, 105, 1, Fields, Cmd)
#define MeCom_COM_ErrorInstance(Address, Fields, Cmd)                   MeCom_ParValuel(Address, 106, 1, Fields, Cmd)
#define MeCom_COM_ErrorParameter(Address, Fields, Cmd)                  MeCom_ParValuel(Address, 107, 1, Fields, Cmd)
#define MeCom_COM_ParameterSystemFlashSaveOff(Address, Fields, Cmd)     MeCom_ParValuel(Address, 108, 1, Fields, Cmd)
#define MeCom_COM_ParameterSystemFlashStatus(Address, Fields, Cmd)      MeCom_ParValuel(Address, 109, 1, Fields, Cmd)

//**************************************************************************
//**********Definition of all LDD Parameter Numbers*************************
//**************************************************************************

//Tab: Monitor Parameters
#define MeCom_LDD_Mon_DeviceType(Address, Value, Cmd)                               MeCom_ParValuel(Address, 1000, 1, Value, Cmd)
#define MeCom_LDD_Mon_SerialNumber(Address, Value, Cmd)                             MeCom_ParValuel(Address, 1001, 1, Value, Cmd)
#define MeCom_LDD_Mon_HardwareVersion(Address, Value, Cmd)                          MeCom_ParValuel(Address, 1002, 1, Value, Cmd)
#define MeCom_LDD_Mon_FirmwareVersion(Address, Value, Cmd)                          MeCom_ParValuel(Address, 1003, 1, Value, Cmd)
#define MeCom_LDD_Mon_FirmwareBuild(Address, Value, Cmd)                            MeCom_ParValuel(Address, 1004, 1, Value, Cmd)
#define MeCom_LDD_Mon_FPGAVersion(Address, Value, Cmd)                              MeCom_ParValuel(Address, 1005, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodeCurrent(Address, Value, Cmd)                        MeCom_ParValuef(Address, 1016, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodeVoltage(Address, Value, Cmd)                        MeCom_ParValuef(Address, 1017, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodeTemperature(Address, Value, Cmd)                    MeCom_ParValuef(Address, 1015, 1, Value, Cmd)
#define MeCom_LDD_Mon_PhotoDiodeCurrent(Address, Value, Cmd)                        MeCom_ParValuef(Address, 1060, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserPower(Address, Value, Cmd)                               MeCom_ParValuef(Address, 1061, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodecurrentCW(Address, Value, Cmd)                      MeCom_ParValuef(Address, 1011, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodeCurrentActual(Address, Value, Cmd)                  MeCom_ParValuef(Address, 1010, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodeVoltageActual(Address, Value, Cmd)                  MeCom_ParValuef(Address, 1013, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodeCurrentPulse(Address, Value, Cmd)                   MeCom_ParValuef(Address, 1012, 1, Value, Cmd)
#define MeCom_LDD_Mon_LaserDiodeVoltagePulse(Address, Value, Cmd)                   MeCom_ParValuef(Address, 1014, 1, Value, Cmd)
#define MeCom_LDD_Mon_DriverInputVoltage(Address, Value, Cmd)                       MeCom_ParValuef(Address, 1020, 1, Value, Cmd)
#define MeCom_LDD_Mon_10VInternalSupply(Address, Value, Cmd)                        MeCom_ParValuef(Address, 1021, 1, Value, Cmd)
#define MeCom_LDD_Mon_3_3VInternalSupply(Address, Value, Cmd)                       MeCom_ParValuef(Address, 1022, 1, Value, Cmd)
#define MeCom_LDD_Mon_1_2VInternalSupply(Address, Value, Cmd)                       MeCom_ParValuef(Address, 1023, 1, Value, Cmd)
#define MeCom_LDD_Mon_ErrorNumber(Address, Value, Cmd)                              MeCom_ParValuel(Address, 1030, 1, Value, Cmd)
#define MeCom_LDD_Mon_ErrorInstance(Address, Value, Cmd)                            MeCom_ParValuel(Address, 1031, 1, Value, Cmd)
#define MeCom_LDD_Mon_ErrorParameter(Address, Value, Cmd)                           MeCom_ParValuel(Address, 1032, 1, Value, Cmd)
#define MeCom_LDD_Mon_BuckConverter1Current(Address, Value, Cmd)                    MeCom_ParValuef(Address, 1040, 1, Value, Cmd)
#define MeCom_LDD_Mon_BuckConverter2Current(Address, Value, Cmd)                    MeCom_ParValuef(Address, 1041, 1, Value, Cmd)
#define MeCom_LDD_Mon_BuckConverter3Current(Address, Value, Cmd)                    MeCom_ParValuef(Address, 1042, 1, Value, Cmd)
#define MeCom_LDD_Mon_BasePlateTemperature(Address, Value, Cmd)                     MeCom_ParValuef(Address, 1043, 1, Value, Cmd)
#define MeCom_LDD_Mon_DriverStatus(Address, Value, Cmd)                             MeCom_ParValuel(Address, 1050, 1, Value, Cmd)
#define MeCom_LDD_Mon_ParameterSystemFlashStatus(Address, Value, Cmd)               MeCom_ParValuel(Address, 1051, 1, Value, Cmd)

//Tab: Operation Control
#define MeCom_LDD_Ope_CurrentInputSource(Address, Value, Cmd)                       MeCom_ParValuel(Address, 2000, 1, Value, Cmd)
#define MeCom_LDD_Ope_CurrentCW(Address, Value, Cmd)                                MeCom_ParValuef(Address, 2001, 1, Value, Cmd)
#define MeCom_LDD_Ope_CurrentHigh(Address, Value, Cmd)                              MeCom_ParValuef(Address, 2002, 1, Value, Cmd)
#define MeCom_LDD_Ope_CurrentLow(Address, Value, Cmd)                               MeCom_ParValuef(Address, 2003, 1, Value, Cmd)
#define MeCom_LDD_Ope_HighTime(Address, Value, Cmd)                                 MeCom_ParValuef(Address, 2004, 1, Value, Cmd)
#define MeCom_LDD_Ope_LowTime(Address, Value, Cmd)                                  MeCom_ParValuef(Address, 2005, 1, Value, Cmd)
#define MeCom_LDD_Ope_RiseTime(Address, Value, Cmd)                                 MeCom_ParValuef(Address, 2006, 1, Value, Cmd)
#define MeCom_LDD_Ope_FallTime(Address, Value, Cmd)                                 MeCom_ParValuef(Address, 2007, 1, Value, Cmd)
#define MeCom_LDD_Ope_Synchronisation(Address, Value, Cmd)                          MeCom_ParValuel(Address, 2008, 1, Value, Cmd)
#define MeCom_LDD_Ope_PulseInputSource(Address, Value, Cmd)                         MeCom_ParValuel(Address, 2010, 1, Value, Cmd)
#define MeCom_LDD_Ope_PulseHighTime(Address, Value, Cmd)                            MeCom_ParValuef(Address, 2011, 1, Value, Cmd)
#define MeCom_LDD_Ope_PulseLowTime(Address, Value, Cmd)                             MeCom_ParValuef(Address, 2012, 1, Value, Cmd)
#define MeCom_LDD_Ope_EnableInputSource(Address, Value, Cmd)                        MeCom_ParValuel(Address, 2020, 1, Value, Cmd)

//Tab: LaserPower Control
#define MeCom_LDD_Las_InputSource(Address, Value, Cmd)                              MeCom_ParValuel(Address, 5000, 1, Value, Cmd)
#define MeCom_LDD_Las_LP_CW(Address, Value, Cmd)                                    MeCom_ParValuef(Address, 5001, 1, Value, Cmd)
#define MeCom_LDD_Las_LP_High(Address, Value, Cmd)                                  MeCom_ParValuef(Address, 5002, 1, Value, Cmd)
#define MeCom_LDD_Las_LP_Low(Address, Value, Cmd)                                   MeCom_ParValuef(Address, 5003, 1, Value, Cmd)
#define MeCom_LDD_Las_HighTime(Address, Value, Cmd)                                 MeCom_ParValuef(Address, 5004, 1, Value, Cmd)
#define MeCom_LDD_Las_LowTime(Address, Value, Cmd)                                  MeCom_ParValuef(Address, 5005, 1, Value, Cmd)
#define MeCom_LDD_Las_RiseTime(Address, Value, Cmd)                                 MeCom_ParValuef(Address, 5006, 1, Value, Cmd)
#define MeCom_LDD_Las_FallTime(Address, Value, Cmd)                                 MeCom_ParValuef(Address, 5007, 1, Value, Cmd)
#define MeCom_LDD_Las_Kp(Address, Value, Cmd)                                       MeCom_ParValuef(Address, 5010, 1, Value, Cmd)
#define MeCom_LDD_Las_Ti(Address, Value, Cmd)                                       MeCom_ParValuef(Address, 5011, 1, Value, Cmd)
#define MeCom_LDD_Las_Td(Address, Value, Cmd)                                       MeCom_ParValuef(Address, 5012, 1, Value, Cmd)
#define MeCom_LDD_Las_SlopeLimit(Address, Value, Cmd)                               MeCom_ParValuef(Address, 5013, 1, Value, Cmd)
#define MeCom_LDD_Las_CurrentLimiterStartValue(Address, Value, Cmd)                 MeCom_ParValuef(Address, 5020, 1, Value, Cmd)
#define MeCom_LDD_Las_CurrentLimiterRamp(Address, Value, Cmd)                       MeCom_ParValuef(Address, 5021, 1, Value, Cmd)
#define MeCom_LDD_Las_LP_SystemScale(Address, Value, Cmd)                           MeCom_ParValuef(Address, 5030, 1, Value, Cmd)

//Tab: Settings
#define MeCom_LDD_Set_Kp(Address, Value, Cmd)                                       MeCom_ParValuef(Address, 3000, 1, Value, Cmd)
#define MeCom_LDD_Set_Ti(Address, Value, Cmd)                                       MeCom_ParValuef(Address, 3001, 1, Value, Cmd)
#define MeCom_LDD_Set_Td(Address, Value, Cmd)                                       MeCom_ParValuef(Address, 3002, 1, Value, Cmd)
#define MeCom_LDD_Set_AnalogCurrentFactor(Address, Value, Cmd)                      MeCom_ParValuef(Address, 3010, 1, Value, Cmd)
#define MeCom_LDD_Set_CurrentLimitMax(Address, Value, Cmd)                          MeCom_ParValuef(Address, 3020, 1, Value, Cmd)
#define MeCom_LDD_Set_CurrentLimitMin(Address, Value, Cmd)                          MeCom_ParValuef(Address, 3021, 1, Value, Cmd)
#define MeCom_LDD_Set_MaxCurrentError(Address, Value, Cmd)                          MeCom_ParValuef(Address, 3022, 1, Value, Cmd)
#define MeCom_LDD_Set_SlopeLimit(Address, Value, Cmd)                               MeCom_ParValuef(Address, 3023, 1, Value, Cmd)
#define MeCom_LDD_Set_PBCResFunc(Address, Value, Cmd)                               MeCom_ParValuel(Address, 3080, 1, Value, Cmd)
#define MeCom_LDD_Set_CommunicationWatchdog(Address, Value, Cmd)                    MeCom_ParValuef(Address, 3030, 1, Value, Cmd)
#define MeCom_LDD_Set_DeviceAddress(Address, Value, Cmd)                            MeCom_ParValuel(Address, 3040, 1, Value, Cmd)
#define MeCom_LDD_Set_RS485CH1BaudRate(Address, Value, Cmd)                         MeCom_ParValuel(Address, 3050, 1, Value, Cmd)
#define MeCom_LDD_Set_RS485CH1ResponseDelay(Address, Value, Cmd)                    MeCom_ParValuef(Address, 3051, 1, Value, Cmd)
#define MeCom_LDD_Set_LaserDiodeTempLowerErrorThreshold(Address, Value, Cmd)        MeCom_ParValuef(Address, 3060, 1, Value, Cmd)
#define MeCom_LDD_Set_LaserDiodeTempUpperErrorThreshold(Address, Value, Cmd)        MeCom_ParValuef(Address, 3061, 1, Value, Cmd)
#define MeCom_LDD_Set_NTCLowerPointTemperature(Address, Value, Cmd)                 MeCom_ParValuef(Address, 3070, 1, Value, Cmd)
#define MeCom_LDD_Set_NTCLowerPointResistance(Address, Value, Cmd)                  MeCom_ParValuef(Address, 3071, 1, Value, Cmd)
#define MeCom_LDD_Set_NTCMiddlePointTemperature(Address, Value, Cmd)                MeCom_ParValuef(Address, 3072, 1, Value, Cmd)
#define MeCom_LDD_Set_NTCMiddlePointResistance(Address, Value, Cmd)                 MeCom_ParValuef(Address, 3073, 1, Value, Cmd)
#define MeCom_LDD_Set_NTCUpperPointTemperature(Address, Value, Cmd)                 MeCom_ParValuef(Address, 3074, 1, Value, Cmd)
#define MeCom_LDD_Set_NTCUpperPointResistance(Address, Value, Cmd)                  MeCom_ParValuef(Address, 3075, 1, Value, Cmd)

//Tab: Expert
#define MeCom_LDD_Exp_LaserDiodeTempADCCalibrationOffset(Address, Value, Cmd)       MeCom_ParValuef(Address, 4000, 1, Value, Cmd)
#define MeCom_LDD_Exp_LaserDiodeTempADCCalibrationGain(Address, Value, Cmd)         MeCom_ParValuef(Address, 4001, 1, Value, Cmd)
#define MeCom_LDD_Exp_LaserPowerMeasurementRs(Address, Value, Cmd)                  MeCom_ParValuef(Address, 4010, 1, Value, Cmd)
#define MeCom_LDD_Exp_CurrentMeasurementOffset(Address, Value, Cmd)                 MeCom_ParValuef(Address, 4020, 1, Value, Cmd)
#define MeCom_LDD_Exp_CurrentMeasurementGain(Address, Value, Cmd)                   MeCom_ParValuef(Address, 4021, 1, Value, Cmd)
#define MeCom_LDD_Exp_LaserPowerMeasurementOffset(Address, Value, Cmd)              MeCom_ParValuef(Address, 4030, 1, Value, Cmd)
#define MeCom_LDD_Exp_LaserPowerMeasurementGain(Address, Value, Cmd)                MeCom_ParValuef(Address, 4031, 1, Value, Cmd)
#define MeCom_LDD_Exp_ParallelFunctionType(Address, Value, Cmd)                     MeCom_ParValuel(Address, 4100, 1, Value, Cmd)
#define MeCom_LDD_Exp_ParallelRS485Ch(Address, Value, Cmd)                          MeCom_ParValuel(Address, 4101, 1, Value, Cmd)
#define MeCom_LDD_Exp_ParallelNrOfSlaves(Address, Value, Cmd)                       MeCom_ParValuel(Address, 4102, 1, Value, Cmd)
#define MeCom_LDD_Exp_ParallelSlaveID(Address, Value, Cmd)                          MeCom_ParValuel(Address, 4103, 1, Value, Cmd)

//Not in Service Software displayed Parameters
#define MeCom_LDD_Oth_CurrentWave_Current(Address, Value, Cmd)                      MeCom_ParValuef(Address, 50000, 1, Value, Cmd)
#define MeCom_LDD_Oth_CurrentWave_Pulse(Address, Value, Cmd)                        MeCom_ParValuel(Address, 50001, 1, Value, Cmd)
#define MeCom_LDD_Oth_CurrentWave_Enable(Address, Value, Cmd)                       MeCom_ParValuel(Address, 50002, 1, Value, Cmd)
#define MeCom_LDD_Oth_CurrentWave_Light(Address, Value, Cmd)                        MeCom_ParValuef(Address, 50003, 1, Value, Cmd)



//**************************************************************************
//**********Definition of all TEC Parameter Numbers*************************
//**************************************************************************

//Tab: Monitor Parameters
#define MeCom_TEC_Mon_ObjectTemperature(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 1000, Inst, Value, Cmd)
#define MeCom_TEC_Mon_SinkTemperature(Address, Inst, Value, Cmd)                    MeCom_ParValuef(Address, 1001, Inst, Value, Cmd)
#define MeCom_TEC_Mon_TargetObjectTemperature(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 1010, Inst, Value, Cmd)
#define MeCom_TEC_Mon_RampNominalObjectTemperature(Address, Inst, Value, Cmd)       MeCom_ParValuef(Address, 1011, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ThermalPowerModelCurrent(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 1012, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ActualOutputCurrent(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 1020, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ActualOutputVoltage(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 1021, Inst, Value, Cmd)
#define MeCom_TEC_Mon_PIDLowerLimitation(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 1030, Inst, Value, Cmd)
#define MeCom_TEC_Mon_PIDUpperLimitation(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 1031, Inst, Value, Cmd)
#define MeCom_TEC_Mon_PIDControlVariable(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 1032, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ObjectSensorRawADCValue(Address, Inst, Value, Cmd)            MeCom_ParValuel(Address, 1040, Inst, Value, Cmd)
#define MeCom_TEC_Mon_SinkSensorRawADCValue(Address, Inst, Value, Cmd)              MeCom_ParValuel(Address, 1041, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ObjectSensorResistance(Address, Inst, Value, Cmd)             MeCom_ParValuef(Address, 1042, Inst, Value, Cmd)
#define MeCom_TEC_Mon_SinkSensorResitance(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 1043, Inst, Value, Cmd)
#define MeCom_TEC_Mon_SinkSensorTemperature(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 1044, Inst, Value, Cmd)
#define MeCom_TEC_Mon_FirmwareVersion(Address, Inst, Value, Cmd)                    MeCom_ParValuel(Address, 1050, Inst, Value, Cmd)
#define MeCom_TEC_Mon_FirmwareBuildNumber(Address, Inst, Value, Cmd)                MeCom_ParValuel(Address, 1051, Inst, Value, Cmd)
#define MeCom_TEC_Mon_HardwareVersion(Address, Inst, Value, Cmd)                    MeCom_ParValuel(Address, 1052, Inst, Value, Cmd)
#define MeCom_TEC_Mon_SerialNumber(Address, Inst, Value, Cmd)                       MeCom_ParValuel(Address, 1053, Inst, Value, Cmd)
#define MeCom_TEC_Mon_DriverInputVoltage(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 1060, Inst, Value, Cmd)
#define MeCom_TEC_Mon_MedVInternalSupply(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 1061, Inst, Value, Cmd)
#define MeCom_TEC_Mon_3_3VInternalSupply(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 1062, Inst, Value, Cmd)
#define MeCom_TEC_Mon_BasePlateTemperature(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 1063, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ErrorNumber(Address, Inst, Value, Cmd)                        MeCom_ParValuel(Address, 1070, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ErrorInstance(Address, Inst, Value, Cmd)                      MeCom_ParValuel(Address, 1071, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ErrorParameter(Address, Inst, Value, Cmd)                     MeCom_ParValuel(Address, 1072, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ParallelActualOutputCurrent(Address, Inst, Value, Cmd)        MeCom_ParValuef(Address, 1090, Inst, Value, Cmd)
#define MeCom_TEC_Mon_DriverStatus(Address, Inst, Value, Cmd)                       MeCom_ParValuel(Address, 1080, Inst, Value, Cmd)
#define MeCom_TEC_Mon_ParameterSystemFlashStatus(Address, Inst, Value, Cmd)         MeCom_ParValuel(Address, 1081, Inst, Value, Cmd)
#define MeCom_TEC_Mon_FanRelativeCoolingPower(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 1100, Inst, Value, Cmd)
#define MeCom_TEC_Mon_FanNominalFanSpeed(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 1101, Inst, Value, Cmd)
#define MeCom_TEC_Mon_FanActualFanSpeed(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 1102, Inst, Value, Cmd)
#define MeCom_TEC_Mon_FanActualPwmLevel(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 1103, Inst, Value, Cmd)
#define MeCom_TEC_Mon_TemperatureIsStable(Address, Inst, Value, Cmd)                MeCom_ParValuel(Address, 1200, Inst, Value, Cmd)

//Tab: Operation Parameters
#define MeCom_TEC_Ope_OutputStageInputSelection(Address, Inst, Value, Cmd)          MeCom_ParValuel(Address, 2000, Inst, Value, Cmd)
#define MeCom_TEC_Ope_OutputStageEnable(Address, Inst, Value, Cmd)                  MeCom_ParValuel(Address, 2010, Inst, Value, Cmd)
#define MeCom_TEC_Ope_SetStaticCurrent(Address, Inst, Value, Cmd)                   MeCom_ParValuef(Address, 2020, Inst, Value, Cmd)
#define MeCom_TEC_Ope_SetStaticVoltage(Address, Inst, Value, Cmd)                   MeCom_ParValuef(Address, 2021, Inst, Value, Cmd)
#define MeCom_TEC_Ope_CurrentLimitation(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 2030, Inst, Value, Cmd)
#define MeCom_TEC_Ope_VoltageLimitation(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 2031, Inst, Value, Cmd)
#define MeCom_TEC_Ope_CurrentErrorThreshold(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 2032, Inst, Value, Cmd)
#define MeCom_TEC_Ope_VoltageErrorThreshold(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 2033, Inst, Value, Cmd)
#define MeCom_TEC_Ope_GeneralOperatingMode(Address, Inst, Value, Cmd)               MeCom_ParValuel(Address, 2040, Inst, Value, Cmd)
#define MeCom_TEC_Ope_DeviceAddress(Address, Inst, Value, Cmd)                      MeCom_ParValuel(Address, 2051, Inst, Value, Cmd)
#define MeCom_TEC_Ope_RS485CH1BaudRate(Address, Inst, Value, Cmd)                   MeCom_ParValuel(Address, 2050, Inst, Value, Cmd)
#define MeCom_TEC_Ope_RS485CH1ResponseDelay(Address, Inst, Value, Cmd)              MeCom_ParValuel(Address, 2052, Inst, Value, Cmd)
#define MeCom_TEC_Ope_ComWatchDogTimeout(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 2060, Inst, Value, Cmd)

//Tab Temperature Control
#define MeCom_TEC_Tem_TargetObjectTemp(Address, Inst, Value, Cmd)                   MeCom_ParValuef(Address, 3000, Inst, Value, Cmd)
#define MeCom_TEC_Tem_CoarseTempRamp(Address, Inst, Value, Cmd)                     MeCom_ParValuef(Address, 3003, Inst, Value, Cmd)
#define MeCom_TEC_Tem_ProximityWidth(Address, Inst, Value, Cmd)                     MeCom_ParValuef(Address, 3002, Inst, Value, Cmd)
#define MeCom_TEC_Tem_Kp(Address, Inst, Value, Cmd)                                 MeCom_ParValuef(Address, 3010, Inst, Value, Cmd)
#define MeCom_TEC_Tem_Ti(Address, Inst, Value, Cmd)                                 MeCom_ParValuef(Address, 3011, Inst, Value, Cmd)
#define MeCom_TEC_Tem_Td(Address, Inst, Value, Cmd)                                 MeCom_ParValuef(Address, 3012, Inst, Value, Cmd)
#define MeCom_TEC_Tem_DPartDampPT1(Address, Inst, Value, Cmd)                       MeCom_ParValuef(Address, 3013, Inst, Value, Cmd)
#define MeCom_TEC_Tem_ModelizationMode(Address, Inst, Value, Cmd)                   MeCom_ParValuel(Address, 3020, Inst, Value, Cmd)
#define MeCom_TEC_Tem_PeltierMaxCurrent(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 3030, Inst, Value, Cmd)
#define MeCom_TEC_Tem_PeltierMaxVoltage(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 3031, Inst, Value, Cmd)
#define MeCom_TEC_Tem_PeltierCoolingCapacity(Address, Inst, Value, Cmd)             MeCom_ParValuef(Address, 3032, Inst, Value, Cmd)
#define MeCom_TEC_Tem_PeltierDeltaTemperature(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 3033, Inst, Value, Cmd)
#define MeCom_TEC_Tem_PeltierPositiveCurrentIs(Address, Inst, Value, Cmd)           MeCom_ParValuel(Address, 3034, Inst, Value, Cmd)
#define MeCom_TEC_Tem_ResistorResistance(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 3040, Inst, Value, Cmd)
#define MeCom_TEC_Tem_ResistorMaxCurrent(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 3041, Inst, Value, Cmd)

//Tab Object Temperature
#define MeCom_TEC_Obj_TemperatureOffset(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 4001, Inst, Value, Cmd)
#define MeCom_TEC_Obj_TemperatureGain(Address, Inst, Value, Cmd)                    MeCom_ParValuef(Address, 4002, Inst, Value, Cmd)
#define MeCom_TEC_Obj_LowerErrorThreshold(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 4010, Inst, Value, Cmd)
#define MeCom_TEC_Obj_UpperErrorThreshold(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 4011, Inst, Value, Cmd)
#define MeCom_TEC_Obj_MaxTempChange(Address, Inst, Value, Cmd)                      MeCom_ParValuef(Address, 4012, Inst, Value, Cmd)
#define MeCom_TEC_Obj_NTCLowerPointTemperature(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 4020, Inst, Value, Cmd)
#define MeCom_TEC_Obj_NTCLowerPointResistance(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 4021, Inst, Value, Cmd)
#define MeCom_TEC_Obj_NTCMiddlePointTemperature(Address, Inst, Value, Cmd)          MeCom_ParValuef(Address, 4022, Inst, Value, Cmd)
#define MeCom_TEC_Obj_NTCMiddlePointResistance(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 4023, Inst, Value, Cmd)
#define MeCom_TEC_Obj_NTCUpperPointTemperature(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 4024, Inst, Value, Cmd)
#define MeCom_TEC_Obj_NTCUpperPointResistance(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 4025, Inst, Value, Cmd)
#define MeCom_TEC_Obj_StabilityTemperatureWindow(Address, Inst, Value, Cmd)         MeCom_ParValuef(Address, 4040, Inst, Value, Cmd)
#define MeCom_TEC_Obj_StabilityMinTimeInWindow(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 4041, Inst, Value, Cmd)
#define MeCom_TEC_Obj_StabilityMaxStabiTime(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 4042, Inst, Value, Cmd)
#define MeCom_TEC_Obj_MeasLowestResistance(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 4030, Inst, Value, Cmd)
#define MeCom_TEC_Obj_MeasHighestResistance(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 4031, Inst, Value, Cmd)
#define MeCom_TEC_Obj_MeasTempAtLowestResistance(Address, Inst, Value, Cmd)         MeCom_ParValuef(Address, 4032, Inst, Value, Cmd)
#define MeCom_TEC_Obj_MeasTempAtHighestResistance(Address, Inst, Value, Cmd)        MeCom_ParValuef(Address, 4033, Inst, Value, Cmd)

//Tab Sink Temperature
#define MeCom_TEC_Sin_TemperatureOffset(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 5001, Inst, Value, Cmd)
#define MeCom_TEC_Sin_TemperatureGain(Address, Inst, Value, Cmd)                    MeCom_ParValuef(Address, 5002, Inst, Value, Cmd)
#define MeCom_TEC_Sin_LowerErrorThreshold(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 5010, Inst, Value, Cmd)
#define MeCom_TEC_Sin_UpperErrorThreshold(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 5011, Inst, Value, Cmd)
#define MeCom_TEC_Sin_MaxTempChange(Address, Inst, Value, Cmd)                      MeCom_ParValuef(Address, 5012, Inst, Value, Cmd)
#define MeCom_TEC_Sin_NTCLowerPointTemperature(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 5020, Inst, Value, Cmd)
#define MeCom_TEC_Sin_NTCLowerPointResistance(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 5021, Inst, Value, Cmd)
#define MeCom_TEC_Sin_NTCMiddlePointTemperature(Address, Inst, Value, Cmd)          MeCom_ParValuef(Address, 5022, Inst, Value, Cmd)
#define MeCom_TEC_Sin_NTCMiddlePointResistance(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 5023, Inst, Value, Cmd)
#define MeCom_TEC_Sin_NTCUpperPointTemperature(Address, Inst, Value, Cmd)           MeCom_ParValuef(Address, 5024, Inst, Value, Cmd)
#define MeCom_TEC_Sin_NTCUpperPointResistance(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 5025, Inst, Value, Cmd)
#define MeCom_TEC_Sin_SinkTemperatureSelection(Address, Inst, Value, Cmd)           MeCom_ParValuel(Address, 5030, Inst, Value, Cmd)
#define MeCom_TEC_Sin_FixedTemperature(Address, Inst, Value, Cmd)                   MeCom_ParValuef(Address, 5031, Inst, Value, Cmd)
#define MeCom_TEC_Sin_MeasLowestResistance(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 5040, Inst, Value, Cmd)
#define MeCom_TEC_Sin_MeasHighestResistance(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 5041, Inst, Value, Cmd)
#define MeCom_TEC_Sin_MeasTempAtLowestResistance(Address, Inst, Value, Cmd)         MeCom_ParValuef(Address, 5042, Inst, Value, Cmd)
#define MeCom_TEC_Sin_MeasTempAtHighestResistance(Address, Inst, Value, Cmd)        MeCom_ParValuef(Address, 5043, Inst, Value, Cmd)

//Tab Expert: Sub Tab Temperature Measurement
#define MeCom_TEC_Exp_ObjMeasPGAGain(Address, Inst, Value, Cmd)                     MeCom_ParValuel(Address, 6000, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ObjMeasCurrentSource(Address, Inst, Value, Cmd)               MeCom_ParValuel(Address, 6001, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ObjMeasADCRs(Address, Inst, Value, Cmd)                       MeCom_ParValuef(Address, 6002, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ObjMeasADCCalibOffset(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 6003, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ObjMeasADCCalibGain(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 6004, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ObjMeasSensorTypeSelection(Address, Inst, Value, Cmd)         MeCom_ParValuel(Address, 6005, Inst, Value, Cmd)
#define MeCom_TEC_Exp_SinMeasADCRv(Address, Inst, Value, Cmd)                       MeCom_ParValuef(Address, 6010, Inst, Value, Cmd)
#define MeCom_TEC_Exp_SinMeasADCVps(Address, Inst, Value, Cmd)                      MeCom_ParValuef(Address, 6013, Inst, Value, Cmd)
#define MeCom_TEC_Exp_SinMeasADCCalibOffset(Address, Inst, Value, Cmd)              MeCom_ParValuef(Address, 6011, Inst, Value, Cmd)
#define MeCom_TEC_Exp_SinMeasADCCalibGain(Address, Inst, Value, Cmd)                MeCom_ParValuef(Address, 6012, Inst, Value, Cmd)

//Tab Expert: Sub Tab Display
#define MeCom_TEC_Exp_DisplayType(Address, Inst, Value, Cmd)                        MeCom_ParValuel(Address, 6020, Inst, Value, Cmd)
#define MeCom_TEC_Exp_DisplayLineDefText(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 6021, Inst, Value, Cmd)
#define MeCom_TEC_Exp_DisplayLineAltText(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 6022, Inst, Value, Cmd)
#define MeCom_TEC_Exp_DisplayLineAltMode(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 6023, Inst, Value, Cmd)

//Tab Expert: Sub Tab PBC
#define MeCom_TEC_Exp_PbcFunction(Address, Inst, Value, Cmd)                        MeCom_ParValuel(Address, 6100, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ChangeButtonLowTemperature(Address, Inst, Value, Cmd)         MeCom_ParValuef(Address, 6110, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ChangeButtonHighTemperature(Address, Inst, Value, Cmd)        MeCom_ParValuef(Address, 6111, Inst, Value, Cmd)
#define MeCom_TEC_Exp_ChangeButtonStepSize(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 6112, Inst, Value, Cmd)

//Tab Expert: Sub Tab FAN
#define MeCom_TEC_Exp_FanControlEnable(Address, Inst, Value, Cmd)                   MeCom_ParValuel(Address, 6200, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanActualTempSource(Address, Inst, Value, Cmd)                MeCom_ParValuel(Address, 6210, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanTargetTemp(Address, Inst, Value, Cmd)                      MeCom_ParValuef(Address, 6211, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanTempKp(Address, Inst, Value, Cmd)                          MeCom_ParValuef(Address, 6212, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanTempTi(Address, Inst, Value, Cmd)                          MeCom_ParValuef(Address, 6213, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanTempTd(Address, Inst, Value, Cmd)                          MeCom_ParValuef(Address, 6214, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanSpeedMin(Address, Inst, Value, Cmd)                        MeCom_ParValuef(Address, 6220, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanSpeedMax(Address, Inst, Value, Cmd)                        MeCom_ParValuef(Address, 6221, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanSpeedKp(Address, Inst, Value, Cmd)                         MeCom_ParValuef(Address, 6222, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanSpeedTi(Address, Inst, Value, Cmd)                         MeCom_ParValuef(Address, 6223, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanSpeedTd(Address, Inst, Value, Cmd)                         MeCom_ParValuef(Address, 6224, Inst, Value, Cmd)
#define MeCom_TEC_Exp_FanSpeedBypass(Address, Inst, Value, Cmd)                     MeCom_ParValuel(Address, 6225, Inst, Value, Cmd)
#define MeCom_TEC_Exp_PwmFrequency(Address, Inst, Value, Cmd)                       MeCom_ParValuel(Address, 6230, Inst, Value, Cmd)

//Tab Expert: Sub Tab Misc
#define MeCom_TEC_Exp_MiscActObjectTempSource(Address, Inst, Value, Cmd)            MeCom_ParValuel(Address, 6300, Inst, Value, Cmd)
#define MeCom_TEC_Exp_MiscDelayTillReset(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 6310, Inst, Value, Cmd)
#define MeCom_TEC_Exp_MiscError108Delay(Address, Inst, Value, Cmd)                  MeCom_ParValuel(Address, 6320, Inst, Value, Cmd)

//Other Parameters (Not directly displayed in the Service Software)
#define MeCom_TEC_Oth_LiveEnable(Address, Inst, Value, Cmd)                         MeCom_ParValuel(Address, 50000, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LiveSetCurrent(Address, Inst, Value, Cmd)                     MeCom_ParValuef(Address, 50001, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LiveSetVoltage(Address, Inst, Value, Cmd)                     MeCom_ParValuef(Address, 50002, Inst, Value, Cmd)
#define MeCom_TEC_Oth_SineRampStartPoint(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 50010, Inst, Value, Cmd)
#define MeCom_TEC_Oth_ObjectTargetTempSourceSelection(Address, Inst, Value, Cmd)    MeCom_ParValuel(Address, 50011, Inst, Value, Cmd)
#define MeCom_TEC_Oth_ObjectTargetTemperature(Address, Inst, Value, Cmd)            MeCom_ParValuef(Address, 50012, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmAutoTuningStart(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 51000, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmAutoTuningCancel(Address, Inst, Value, Cmd)                MeCom_ParValuel(Address, 51001, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmThermalModelSpeed(Address, Inst, Value, Cmd)               MeCom_ParValuel(Address, 51002, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmTuningParameter2A(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 51010, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmTuningParameter2D(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 51011, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmTuningParameterKu(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 51012, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmTuningParameterTu(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 51013, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmPIDParameterKp(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 51014, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmPIDParameterTi(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 51015, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmPIDParameterTd(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 51016, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmSlowPIParameterKp(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 51022, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmSlowPIParameterTi(Address, Inst, Value, Cmd)               MeCom_ParValuef(Address, 51023, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmPIDDPartDamping(Address, Inst, Value, Cmd)                 MeCom_ParValuef(Address, 51024, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmCoarseTempRamp(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 51017, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmProximityWidth(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 51018, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmTuningStatus(Address, Inst, Value, Cmd)                    MeCom_ParValuel(Address, 51020, Inst, Value, Cmd)
#define MeCom_TEC_Oth_AtmTuningProgress(Address, Inst, Value, Cmd)                  MeCom_ParValuef(Address, 51021, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LutTableStart(Address, Inst, Value, Cmd)                      MeCom_ParValuel(Address, 52000, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LutTableStop(Address, Inst, Value, Cmd)                       MeCom_ParValuel(Address, 52001, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LutTableStatus(Address, Inst, Value, Cmd)                     MeCom_ParValuel(Address, 52002, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LutCurrentTableLine(Address, Inst, Value, Cmd)                MeCom_ParValuel(Address, 52003, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LutTableIDSelection(Address, Inst, Value, Cmd)                MeCom_ParValuel(Address, 52010, Inst, Value, Cmd)
#define MeCom_TEC_Oth_LutNrOfRepetitions(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 52012, Inst, Value, Cmd)
#define MeCom_TEC_Oth_PbcEnableFunction(Address, Inst, Value, Cmd)                  MeCom_ParValuel(Address, 52100, Inst, Value, Cmd)
#define MeCom_TEC_Oth_PbcSetOutputToPushPull(Address, Inst, Value, Cmd)             MeCom_ParValuel(Address, 52101, Inst, Value, Cmd)
#define MeCom_TEC_Oth_PbcSetOutputStates(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 52102, Inst, Value, Cmd)
#define MeCom_TEC_Oth_PbcReadInputStates(Address, Inst, Value, Cmd)                 MeCom_ParValuel(Address, 52103, Inst, Value, Cmd)
#define MeCom_TEC_Oth_ExternalActualObjectTemperature(Address, Inst, Value, Cmd)    MeCom_ParValuef(Address, 52200, Inst, Value, Cmd)

#endif
