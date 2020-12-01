#ifndef MEFRAME_H
#define MEFRAME_H

#include "../MePort.h"

struct MeFrame_RcvFrameS
{
    uint8_t DataReceived;
    uint8_t AckReceived;
    uint8_t Address;
    uint16_t SeqNr;
    int8_t Payload[MEPORT_MAX_RX_BUF_SIZE];
};

extern void MeFrame_Send(int8_t Control, uint8_t Address, uint32_t Length, uint16_t SeqNr, int8_t *Payload);
extern void MeFrame_Receive(int8_t in);

extern struct MeFrame_RcvFrameS MeFrame_RcvFrame;

#endif