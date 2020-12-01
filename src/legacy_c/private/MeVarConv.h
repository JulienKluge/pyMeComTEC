#ifndef MEVARCONV_H
#define MEVARCONV_H

#include <stdint.h>

extern int8_t MeVarConv_UcToHEX(uint8_t value);

extern uint8_t  MeVarConv_HexToDigit(int8_t *arr);
extern uint8_t  MeVarConv_HexToUc   (int8_t *arr);
extern int8_t   MeVarConv_HexToSc   (int8_t *arr);
extern uint16_t MeVarConv_HexToUs   (int8_t *arr);
extern int16_t  MeVarConv_HexToSs   (int8_t *arr);
extern uint32_t MeVarConv_HexToUl   (int8_t *arr);
extern int32_t  MeVarConv_HexToSl   (int8_t *arr);
extern float    MeVarConv_HexToFloat(int8_t *arr);

extern void MeVarConv_AddDigitHex   (int8_t *arr, uint8_t  value);
extern void MeVarConv_AddUcHex      (int8_t *arr, uint8_t  value);
extern void MeVarConv_AddScHex      (int8_t *arr, int8_t   value);
extern void MeVarConv_AddUsHex      (int8_t *arr, uint16_t value);
extern void MeVarConv_AddSsHex      (int8_t *arr, int16_t  value);
extern void MeVarConv_AddUlHex      (int8_t *arr, uint32_t value);
extern void MeVarConv_AddSlHex      (int8_t *arr, int32_t  value);
extern void MeVarConv_AddFloatHex   (int8_t *arr, float    value);

#endif