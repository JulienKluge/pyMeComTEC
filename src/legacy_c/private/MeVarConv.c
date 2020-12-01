 /*==============================================================================*/
/** @file       VarConvert.c
    @brief      Converts the variables for the communication
    @author     Meerstetter Engineering GmbH: Marc Luethi

*/

/*==============================================================================*/
/*                          IMPORT                                              */
/*==============================================================================*/
#include "MeVarConv.h"
#include <string.h>

/*==============================================================================*/
/*                          DEFINITIONS/DECLARATIONS                            */
/*==============================================================================*/

/*==============================================================================*/
/*                          STATIC FUNCTION PROTOTYPES                          */
/*==============================================================================*/
static uint8_t HEXtoNR(int8_t uc);

/*==============================================================================*/
/*                          EXTERN VARIABLES                                    */
/*==============================================================================*/
static const int8_t cHex[16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};

/*==============================================================================*/
/*                          STATIC  VARIABLES                                   */
/*==============================================================================*/

/*======================================================================*/
int8_t   MeVarConv_UcToHEX   (uint8_t value)
{
    if(value > 0x0F) return 'X';
    return cHex[value];
}

/*======================================================================*/
uint8_t  MeVarConv_HexToDigit(int8_t *arr)
{
	return HEXtoNR(*arr);
}
/*======================================================================*/
uint8_t  MeVarConv_HexToUc   (int8_t *arr)
{
	return (HEXtoNR(*arr)*16) + HEXtoNR(*(arr+1));
}
/*======================================================================*/
int8_t   MeVarConv_HexToSc   (int8_t *arr)
{
    return (int8_t)(((HEXtoNR(arr[0])&0x0F)*16)+ HEXtoNR(arr[1]));
}
/*======================================================================*/
uint16_t MeVarConv_HexToUs   (int8_t *arr)
{
	return (HEXtoNR(*(arr+0))*4096)+ (HEXtoNR(*(arr+1))*256)+ (HEXtoNR(*(arr+2))*16)+ (HEXtoNR(*(arr+3)));
}
/*======================================================================*/
int16_t  MeVarConv_HexToSs   (int8_t *arr)
{
	return (((int16_t)HEXtoNR(arr[0])<<12)+ ((int16_t)HEXtoNR(arr[1])<<8)+ ((int16_t)HEXtoNR(arr[2])<<4)+ (int16_t)HEXtoNR(arr[3]));
}
/*======================================================================*/
uint32_t MeVarConv_HexToUl   (int8_t *arr)
{
	return 
        (((uint32_t)HEXtoNR(arr[0])<<28)   + ((uint32_t)HEXtoNR(arr[1])<<24)+  
        ((uint32_t)HEXtoNR(arr[2])<<20)    + ((uint32_t)HEXtoNR(arr[3])<<16)+
		((uint32_t)HEXtoNR(arr[4])<<12)    + ((uint32_t)HEXtoNR(arr[5])<<8)+ 
        ((uint32_t)HEXtoNR(arr[6])<<4)     +  (uint32_t)HEXtoNR(arr[7]));
}
/*======================================================================*/
int32_t  MeVarConv_HexToSl   (int8_t *arr)
{
	return 
        (((int32_t)HEXtoNR(arr[0])<<28)    + ((int32_t)HEXtoNR(arr[1])<<24)+  
        ((int32_t)HEXtoNR(arr[2])<<20)     + ((int32_t)HEXtoNR(arr[3])<<16)+
		((int32_t)HEXtoNR(arr[4])<<12)     + ((int32_t)HEXtoNR(arr[5])<<8)+ 
        ((int32_t)HEXtoNR(arr[6])<<4)      + (int32_t)HEXtoNR(arr[7]));
}
/*======================================================================*/
float    MeVarConv_HexToFloat(int8_t *arr)
{
    uint32_t temp;
    float fpv;
    temp = MeVarConv_HexToUl(arr);
    memcpy(&fpv, &temp, sizeof(fpv));
    return fpv;
}
/*======================================================================*/
void MeVarConv_AddDigitHex   (int8_t *arr, uint8_t  value)
{
	*arr = cHex[value]; arr++;
}
/*======================================================================*/
void MeVarConv_AddUcHex      (int8_t *arr, uint8_t  value)
{
	*arr = cHex[value/16]; arr++;
	*arr = cHex[value%16]; arr++;
}
/*======================================================================*/
void MeVarConv_AddScHex      (int8_t *arr, int8_t   value)
{
    uint8_t us = (uint8_t)value;
    *arr = cHex[(us>>4)&0x00F]; arr++;
    *arr = cHex[(us   )&0x00F]; arr++;
}
/*======================================================================*/
void MeVarConv_AddUsHex      (int8_t *arr, uint16_t value)
{
	value = value & 0x0000FFFF;
	*arr = cHex[value/4096]; arr++;
	*arr = cHex[(value/256)%16]; arr++;
	*arr = cHex[(value%256)/16]; arr++;
	*arr = cHex[(value%256)%16]; arr++;
}
/*======================================================================*/
void MeVarConv_AddSsHex      (int8_t *arr, int16_t  value)
{
    uint16_t us = (uint16_t)value;
	*arr = cHex[(us>>12)&0x00F]; arr++;
	*arr = cHex[(us>>8)&0x00F]; arr++;
	*arr = cHex[(us>>4)&0x00F]; arr++;
	*arr = cHex[(us   )&0x00F]; arr++;
}
/*======================================================================*/
void MeVarConv_AddUlHex      (int8_t *arr, uint32_t value)
{
	*arr = cHex[value>>28]; arr++;
	*arr = cHex[(value>>24)&0x00F]; arr++;
	*arr = cHex[(value>>20)&0x00F]; arr++;
	*arr = cHex[(value>>16)&0x00F]; arr++;
	*arr = cHex[(value>>12)&0x00F]; arr++;
	*arr = cHex[(value>>8)&0x00F]; arr++;
	*arr = cHex[(value>>4)&0x00F]; arr++;
	*arr = cHex[(value   )&0x00F]; arr++;
}

/*======================================================================*/
void MeVarConv_AddSlHex      (int8_t *arr, int32_t  value)
{
    uint32_t ul = (uint32_t)value;
	*arr = cHex[ul>>28]; arr++;
	*arr = cHex[(ul>>24)&0x00F]; arr++;
	*arr = cHex[(ul>>20)&0x00F]; arr++;
	*arr = cHex[(ul>>16)&0x00F]; arr++;
	*arr = cHex[(ul>>12)&0x00F]; arr++;
	*arr = cHex[(ul>>8)&0x00F]; arr++;
	*arr = cHex[(ul>>4)&0x00F]; arr++;
	*arr = cHex[(ul   )&0x00F]; arr++;
}
/*======================================================================*/
void MeVarConv_AddFloatHex   (int8_t *arr, float    value)
{
    uint32_t lvalue;
    memcpy(&lvalue, &value, sizeof(value));
    MeVarConv_AddUlHex(arr, lvalue);
}

/*======================================================================*/
static uint8_t HEXtoNR(int8_t uc)
{
	switch(uc)
		{
				case '0': return 0;
				case '1': return 1;
				case '2': return 2;
				case '3': return 3;
				case '4': return 4;
				case '5': return 5;
				case '6': return 6;
				case '7': return 7;
				case '8': return 8;
				case '9': return 9;
				case 'A': return 10;
				case 'B': return 11;
				case 'C': return 12;
				case 'D': return 13;
				case 'E': return 14;
				case 'F': return 15;
				case 'a': return 10;
                case 'b': return 11;
                case 'c': return 12;
                case 'd': return 13;
                case 'e': return 14;
                case 'f': return 15;
		}
		return (0);
}

/*==========================EOF=====================================================*/
