/*==============================================================================*/
/** @file       MeFrame.c
    @brief      This file holds the low level protocol functions
    @author     Meerstetter Engineering GmbH: Marc Luethi

    Frame send and receiving Functions.
*/


/*==============================================================================*/
/*                          IMPORT                                              */
/*==============================================================================*/
#include "MeFrame.h"
#include "../MePort.h"
#include "MeCRC16.h"
#include "MeVarConv.h"
#include <string.h>

/*==============================================================================*/
/*                          DEFINITIONS/DECLARATIONS                            */
/*==============================================================================*/


/*==============================================================================*/
/*                          STATIC FUNCTION PROTOTYPES                          */
/*==============================================================================*/

/*==============================================================================*/
/*                          EXTERN VARIABLES                                    */
/*==============================================================================*/
struct MeFrame_RcvFrameS MeFrame_RcvFrame;

/*==============================================================================*/
/*                          STATIC  VARIABLES                                   */
/*==============================================================================*/
static uint16_t LastCRC;

/*==============================================================================*/
/** @brief      Frame Send Function
 *
 *  This function packs the Payload Data into the Frame and calculates the CRC.
 *  The Data is directly passed to the Port Send Byte Function.
 *  The Port Send Function receives the start and End of the Frame information.
 *
*/
void MeFrame_Send(int8_t Control, uint8_t Address, uint32_t Length, uint16_t SeqNr, int8_t *Payload)
{
    uint16_t CRC = 0;
    int8_t txc;

    //Control (Source) Byte
    txc = Control;                              MePort_SendByte(txc, MePort_SB_IsFirstByte); CRC = MeCRC16(CRC, txc);

    //Device Address
    txc = MeVarConv_UcToHEX(Address / 16);      MePort_SendByte(txc, MePort_SB_Normal); CRC = MeCRC16(CRC, txc);
    txc = MeVarConv_UcToHEX(Address % 16);      MePort_SendByte(txc, MePort_SB_Normal); CRC = MeCRC16(CRC, txc);

    //Sequence Number
    txc = MeVarConv_UcToHEX(SeqNr>>12);        MePort_SendByte(txc, MePort_SB_Normal); CRC = MeCRC16(CRC, txc);
    txc = MeVarConv_UcToHEX((SeqNr/256)%16);    MePort_SendByte(txc, MePort_SB_Normal); CRC = MeCRC16(CRC, txc);
    txc = MeVarConv_UcToHEX((SeqNr%256)/16);    MePort_SendByte(txc, MePort_SB_Normal); CRC = MeCRC16(CRC, txc);
    txc = MeVarConv_UcToHEX((SeqNr%256)%16);    MePort_SendByte(txc, MePort_SB_Normal); CRC = MeCRC16(CRC, txc);

    for(uint32_t i = 0; i < Length; i++)
    {
        MePort_SendByte(*Payload, MePort_SB_Normal);
        CRC = MeCRC16(CRC, *Payload);
        Payload++;
    }

    txc = MeVarConv_UcToHEX(CRC>>12);          MePort_SendByte(txc, MePort_SB_Normal); 
    txc = MeVarConv_UcToHEX((CRC/256)%16);      MePort_SendByte(txc, MePort_SB_Normal); 
    txc = MeVarConv_UcToHEX((CRC%256)/16);      MePort_SendByte(txc, MePort_SB_Normal); 
    txc = MeVarConv_UcToHEX((CRC%256)%16);      MePort_SendByte(txc, MePort_SB_Normal); 

    MePort_SendByte(0x0D, MePort_SB_IsLastByte);

    LastCRC = CRC;
}


/*==============================================================================*/
/** @brief      Frame Receive Function
 *
 *  This Function is being called by the receiving function of the target system.
 *  It puts the received bytes back into the frame structure and
 *  checks the CRC. If a complete frame has been received,
 *  the corresponding received Flag is set and
 *  the MePort_SemaphorGive function is being called to unlock
 *  the upper level functions.
 *
*/
void MeFrame_Receive(int8_t in)
{
    static int8_t RcvBuf[MEPORT_MAX_RX_BUF_SIZE + 20];
    static int32_t RcvCtr = -1;

    if(in == '!')
    {
        //Start Indicator --> Reset Receiving Machine
        memset(RcvBuf, 0, sizeof(RcvBuf));
        RcvBuf[0] = in;
        RcvCtr = 1;
        
    }
    else if(in == 0x0D && (RcvCtr >=11))
    {
        //End of a Frame received
        if(RcvCtr == 11)
        {
            //Ack Received

            uint16_t RcvCRC = MeVarConv_HexToUs(&RcvBuf[7]);
            if(RcvCRC == LastCRC && MeFrame_RcvFrame.AckReceived == 0)
            {
                MeFrame_RcvFrame.Address    = MeVarConv_HexToUc(&RcvBuf[1]);
                MeFrame_RcvFrame.SeqNr      = MeVarConv_HexToUs(&RcvBuf[3]);
                MeFrame_RcvFrame.AckReceived = 1;
                MePort_SemaphorGive();
            }
            else RcvCtr = -1; //Error
        }
        else
        {
            //Data Received 

            //Check CRC of received Frame
            uint16_t RcvCRC, CalcCRC = 0;
            for(int32_t i=0; i < (RcvCtr-4); i++) CalcCRC = MeCRC16(CalcCRC, RcvBuf[i]); //Calculate CRC of received Frame
            RcvCRC = MeVarConv_HexToUs(&RcvBuf[RcvCtr-4]); //Get Frame CRC
            if(RcvCRC == CalcCRC && MeFrame_RcvFrame.DataReceived == 0)
            {
                //CRC is correct and all data has been processed
                MeFrame_RcvFrame.Address    = MeVarConv_HexToUc(&RcvBuf[1]);
                MeFrame_RcvFrame.SeqNr      = MeVarConv_HexToUs(&RcvBuf[3]);
                for(int32_t i = 7; i < (RcvCtr-4);  i++)	MeFrame_RcvFrame.Payload[i-7] = RcvBuf[i];
                MeFrame_RcvFrame.DataReceived = 1;
                MePort_SemaphorGive();
            }
        }
    }
    else if(RcvCtr >= 0 && RcvCtr < (MEPORT_MAX_RX_BUF_SIZE+15))
    {
        //Write Data to Buffer
        RcvBuf[RcvCtr] = in;
        RcvCtr++;
    }
    else
    {
        //Error 
        RcvCtr = -1;
    }
}
