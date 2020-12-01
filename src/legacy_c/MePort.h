#ifndef MEPORT_H
#define MEPORT_H

#include <stdint.h>

//This TX Buffer is only used if the Physical Communication Interface receives a string.
//If every byte is directly forwarded to the Interface, this buffer is not needed
#define MEPORT_MAX_TX_BUF_SIZE 100 //Bytes

//This RX Buffer will be allocated 2 times
#define MEPORT_MAX_RX_BUF_SIZE 100 //Bytes

#define MEPORT_SET_AND_QUERY_TIMEOUT 100 //ms

#define MEPORT_ERROR_CMD_NOT_AVAILABLE      1    
#define MEPORT_ERROR_DEVICE_BUSY            2
#define MEPORT_ERROR_GENERAL_COM            3 
#define MEPORT_ERROR_FORMAT                 4 
#define MEPORT_ERROR_PAR_NOT_AVAILABLE      5 
#define MEPORT_ERROR_PAR_NOT_WRITABLE       6 
#define MEPORT_ERROR_PAR_OUT_OF_RANGE       7 
#define MEPORT_ERROR_PAR_INST_NOT_AVAILABLE 8 
#define MEPORT_ERROR_SET_TIMEOUT            20
#define MEPORT_ERROR_QUERY_TIMEOUT          21


typedef enum
{
    MePort_SB_Normal,
    MePort_SB_IsFirstByte,
    MePort_SB_IsLastByte,
} MePort_SB;

extern void MePort_SendByte(int8_t in, MePort_SB FirstLast);
extern void MePort_ReceiveByte(int8_t *arr);
extern void MePort_SemaphorTake(uint32_t TimeoutMs);
extern void MePort_SemaphorGive(void);
extern void MePort_ErrorThrow(int32_t ErrorNr);

#endif
