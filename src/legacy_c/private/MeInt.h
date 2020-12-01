#ifndef MEINT_H
#define MEINT_H

#include <stdint.h>

extern int8_t *MeInt_QueryRcvPayload;

extern uint8_t MeInt_Query(int8_t Control, uint8_t Address, uint32_t Length, int8_t *Payload);
extern uint8_t MeInt_Set(int8_t Control, uint8_t Address, uint32_t Length, int8_t *Payload);


#endif