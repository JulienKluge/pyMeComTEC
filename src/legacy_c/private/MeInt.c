/*==============================================================================*/
/** @file       MeInt.c
    @brief      This file holds the connection oriented  protocol functions
    @author     Meerstetter Engineering GmbH: Marc Luethi

    These Functions do send the given Data down to the Frame level and
    call a wait timeout Function (MePort_SemaphorTake).
    If the timeout has expired without receiving an answer, an error is generated.
    if an answer is received by the lower level functions, the timeout
    function is being unblocked immediately (SemaphoreGive) and the
    received Frame is being checked.

    These functions to try 3 Times. Till a timeout is being generated.

*/


/*==============================================================================*/
/*                          IMPORT                                              */
/*==============================================================================*/
#include "MeInt.h"
#include "MeFrame.h"
#include "MeVarConv.h"

/*==============================================================================*/
/*                          DEFINITIONS/DECLARATIONS                            */
/*==============================================================================*/


/*==============================================================================*/
/*                          STATIC FUNCTION PROTOTYPES                          */
/*==============================================================================*/

/*==============================================================================*/
/*                          EXTERN VARIABLES                                    */
/*==============================================================================*/
int8_t *MeInt_QueryRcvPayload = MeFrame_RcvFrame.Payload;
/*==============================================================================*/
/*                          STATIC  VARIABLES                                   */
/*==============================================================================*/
static uint16_t SequenceNr = 5545; //Initialized to random value

/*==============================================================================*/
/** @brief      Connection Function for Query Commands
 *
*/
uint8_t MeInt_Query(int8_t Control, uint8_t Address, uint32_t Length, int8_t *Payload)
{
    SequenceNr++;

    int32_t Trials = 3;
    while(Trials > 0)
    {
        Trials--;
        MeFrame_RcvFrame.DataReceived = 0;
        MeFrame_RcvFrame.AckReceived = 0;
        MeFrame_Send(Control, Address, Length, SequenceNr, Payload);
        MePort_SemaphorTake(MEPORT_SET_AND_QUERY_TIMEOUT);
        if(MeFrame_RcvFrame.DataReceived == 1 && MeFrame_RcvFrame.Address == Address && MeFrame_RcvFrame.SeqNr == SequenceNr )
        {
            //Correct Data Received -->Check for Error Code
            if(MeFrame_RcvFrame.Payload[0] == '+')
            {
                //Server Error code Received
                MePort_ErrorThrow(MeVarConv_HexToUc(&MeFrame_RcvFrame.Payload[1]));
                return 0;
            }
            return 1;
        }
    }  
    MePort_ErrorThrow(MEPORT_ERROR_QUERY_TIMEOUT);
    return 0;
}

/*==============================================================================*/
/** @brief      Connection Function for Set Commands
 *
*/
uint8_t MeInt_Set(int8_t Control, uint8_t Address, uint32_t Length, int8_t *Payload)
{
    SequenceNr++;

    int32_t Trials = 3;
    while(Trials > 0)
    {
        Trials--;
        MeFrame_RcvFrame.DataReceived = 0;
        MeFrame_RcvFrame.AckReceived = 0;
        MeFrame_Send(Control, Address, Length, SequenceNr, Payload);
        MePort_SemaphorTake(MEPORT_SET_AND_QUERY_TIMEOUT);
        if(MeFrame_RcvFrame.DataReceived == 1 && MeFrame_RcvFrame.Address == Address && MeFrame_RcvFrame.SeqNr == SequenceNr &&
            MeFrame_RcvFrame.Payload[0] == '+')
        {
            //Server Error code Received
            MePort_ErrorThrow(MeVarConv_HexToUc(&MeFrame_RcvFrame.Payload[1]));
            return 0;
        }
        else if(MeFrame_RcvFrame.AckReceived == 1 && MeFrame_RcvFrame.Address == Address && MeFrame_RcvFrame.SeqNr == SequenceNr )
        {
            //Correct ADC received
            return 1;
        }
    }  
    MePort_ErrorThrow(MEPORT_ERROR_SET_TIMEOUT);
    return 0;
}
