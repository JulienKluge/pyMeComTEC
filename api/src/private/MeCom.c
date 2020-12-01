/*==============================================================================*/
/** @file       MeCom.c
    @brief      This file holds the high level protocol functions
    @author     Meerstetter Engineering GmbH: Marc Luethi
    @version    v0.42

    This file holds the functions which should be called by the user application.

*/


/*==============================================================================*/
/*                          IMPORT                                              */
/*==============================================================================*/
#include "../MeCom.h"
#include "MeInt.h"
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

/*==============================================================================*/
/*                          STATIC  VARIABLES                                   */
/*==============================================================================*/


/*==============================================================================*/
/** @brief      Reset Device
 *
*/
uint8_t MeCom_ResetDevice(uint8_t Address)
{
    return MeInt_Set('#', Address, 2, (int8_t*)"RS");
}
/*==============================================================================*/
/** @brief      Return IF String
 *
*/
uint8_t MeCom_GetIdentString(uint8_t Address, int8_t *arr)
{
    uint8_t Succeeded = MeInt_Query('#', Address, 3, (int8_t*)"?IF");
    if(Succeeded == 0) 
    {
        *arr = 0;
        return Succeeded;
    }

    for(int32_t i=0; i<20; i++)
    {
        *arr = MeInt_QueryRcvPayload[i];
        arr++;
    }
    *arr = 0;
    return Succeeded;
}
/*==============================================================================*/
/** @brief      Parameter Set, Get and Limit Get Function for INT32 parameters
 *
 *  Please refer to the "Communication Protocol LDD/TEC Controller" to see
 *  if the INT32 or FLOAT32 function must be used.
 *
 *  This Function does 3 things:
 *  - MeGet:        Queries the actual parameter value
 *  - MeSet:        Sets the given parameter value to the new value
 *  - MeGetLimtis:  Queries the corresponding limits of the parameter
 *
*/
uint8_t MeCom_ParValuel(uint8_t Address, uint16_t ParId, uint8_t Inst, MeParLongFields  *Fields, MeParCmd Cmd)
{
    if(Cmd == MeGet)
    {
        int8_t TxData[20];
        TxData[0] = '?'; TxData[1] = 'V'; TxData[2] = 'R'; 
        MeVarConv_AddUsHex(&TxData[3], ParId);
        MeVarConv_AddUcHex(&TxData[7], Inst);

        uint8_t Succeeded = MeInt_Query('#', Address, 9, TxData);
        if(Succeeded == 0) 
        {
            Fields->Value = 0;
            return Succeeded;
        }

        Fields->Value = MeVarConv_HexToSl(&MeInt_QueryRcvPayload[0]);

        return Succeeded;
    }
    else if(Cmd == MeSet)
    {
        int8_t TxData[20];
        TxData[0] = 'V'; TxData[1] = 'S';
        MeVarConv_AddUsHex(&TxData[2], ParId);
        MeVarConv_AddUcHex(&TxData[6], Inst);
        MeVarConv_AddSlHex(&TxData[8], Fields->Value);

        return MeInt_Set('#', Address, 16, TxData);
    }
    else if(Cmd == MeGetLimits)
    {
        int8_t TxData[20];
        TxData[0] = '?'; TxData[1] = 'V'; TxData[2] = 'L'; 
        MeVarConv_AddUsHex(&TxData[3], ParId);
        MeVarConv_AddUcHex(&TxData[7], Inst);

        uint8_t Succeeded = MeInt_Query('#', Address, 9, TxData);
        if(Succeeded == 0) 
        {
            Fields->Min = 0;
            Fields->Max = 0;
            return Succeeded;
        }

        Fields->Min = MeVarConv_HexToSl(&MeInt_QueryRcvPayload[2]);
        Fields->Max = MeVarConv_HexToSl(&MeInt_QueryRcvPayload[10]);

        return Succeeded;
    }
    return 0;
}
/*==============================================================================*/
/** @brief      Parameter Set, Get and Limit Get Function for FLOAT32 parameters
 *
 *  Please refer to the "Communication Protocol LDD/TEC Controller" to see
 *  if the INT32 or FLOAT32 function must be used.
 *
 *  This function just calls the INT32 Function.
 *
*/
uint8_t MeCom_ParValuef(uint8_t Address, uint16_t ParId, uint8_t Inst, MeParFloatFields *Fields, MeParCmd Cmd)
{
    return MeCom_ParValuel(Address, ParId, Inst, (MeParLongFields *)Fields, Cmd);
}
