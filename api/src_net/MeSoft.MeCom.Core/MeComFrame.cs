using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using MeSoft.MeCom.PhyWrapper;
using System.IO;
using MeSoft.Core.Diagnostics;
using System.Threading;

namespace MeSoft.MeCom.Core
{
    /// <summary>
    /// Handles the communication Frame level of the Meerstetter Engineering GmbH
    /// Communication protocol. 
    /// </summary>
    public class MeComFrame
    {
        IMeComPhy PhyCom;
        Statistics statistics;
        ushort LastCRC = 0;

        /// <summary>
        /// Saves the needed interface internally for further use. 
        /// </summary>
        /// <param name="inPhyCom">Interface to the physical interface.</param>
        /// <param name="statistics">Reference to the Statistics module.</param>
        public MeComFrame(IMeComPhy inPhyCom, Statistics statistics)
        {
            PhyCom = inPhyCom;
            this.statistics = statistics;
        }

        /// <summary>
        /// Serializes the given Data structure to a proper 
        /// frame and sends it to the physical interface. 
        /// It returns immediately. 
        /// </summary>
        /// <param name="txFrame">Data to send.</param>
        /// <exception cref="MeComPhyIntefaceException">Thrown when the underlying physical interface is not or not all bytes were sent.</exception>
        public void SendFrame(MeComPacket txFrame)
        {
            MemoryStream TxStream = new MemoryStream();

            TxStream.WriteByte(Convert.ToByte(txFrame.Control));
            MeComVarConvert.AddUint8(TxStream, (byte)txFrame.Address);
            MeComVarConvert.AddUint16(TxStream, txFrame.SeqNr);
            txFrame.Payload.WriteTo(TxStream);
            LastCRC = CalcCRC_CITT(TxStream);
            MeComVarConvert.AddUint16(TxStream, LastCRC);

            TxStream.WriteByte(0x0D);
            statistics.AddTxBytes(TxStream.Length);
            statistics.IncTxFrames();
            PhyCom.SendString(TxStream);
            TxStream.Position = 0;
            TraceLog.Verbose("Thread: '{0}' TX: {1}", Thread.CurrentThread.Name, new StreamReader(TxStream).ReadToEnd().Replace("\r", "<CR>").Replace("\n", "<LF>"));
        }
        /// <summary>
        /// Receives a correct frame or throws an timeout exception.
        /// </summary>
        /// <returns>Received data.</returns>
        /// <exception cref="MeComPhyIntefaceException">Thrown when the underlying physical interface is not OK.</exception>
        /// <exception cref="MeComPhyTimeoutException">Thrown when no correct frame was received during the specified physical interface timeout.</exception>
        public MeComPacket ReceiveFrameOrTimeout()
        {
            string traceText = "";
            MeComPacket rxFrame = new MeComPacket
            {
                RcvType = ERcvType.Empty
            };
            MemoryStream localRxBuf = null;

            while (rxFrame.RcvType == ERcvType.Empty)
            {
                MemoryStream rxStream = new MemoryStream();
                PhyCom.GetDataOrTimeout(rxStream);
                statistics.AddRxBytes(rxStream.Length);
                rxStream.Position = 0;
                traceText += new StreamReader(rxStream).ReadToEnd().Replace("\r", "<CR>").Replace("\n", "<LF>");
                rxStream.Position = 0;

                while (rxStream.Position < rxStream.Length)
                {
                    byte c = (byte)rxStream.ReadByte();
                    DecodeFrame(ref rxFrame, c, ref localRxBuf);
                    if (rxFrame.RcvType != ERcvType.Empty) break;
                }
            }
            TraceLog.Verbose("Thread: '{0}' RX: {1}", Thread.CurrentThread.Name, traceText);

            return rxFrame;
        }

        private void DecodeFrame(ref MeComPacket RxFrame, byte c, ref MemoryStream LocalRxBuf)
        {
            try
            {
                if (c == Convert.ToByte('!'))
                {
                    //Start indicator
                    LocalRxBuf = new MemoryStream();
                    LocalRxBuf.WriteByte(c);
                }
                else
                {
                    if (c == 0x0D && (LocalRxBuf?.Length >= 11))
                    {
                        //End of Frame received
                        if (LocalRxBuf.Length == 11)
                        {
                            //ACK Received
                            LocalRxBuf.Position = 7;
                            ushort rcvCRC = MeComVarConvert.ReadUint16(LocalRxBuf);
                            if (rcvCRC == LastCRC)
                            {
                                //Valid Ack received --> Extract Data
                                LocalRxBuf.Position = 1;
                                RxFrame.Address = MeComVarConvert.ReadUint8(LocalRxBuf);
                                RxFrame.SeqNr = MeComVarConvert.ReadUint16(LocalRxBuf);
                                RxFrame.RcvType = ERcvType.ACK;
                                statistics.IncRxFrames();
                            }
                        }
                        else
                        {
                            //Data Frame received
                            LocalRxBuf.Position = LocalRxBuf.Length - 4;
                            ushort rcvCRC = MeComVarConvert.ReadUint16(LocalRxBuf);

                            //Cut received CRC form stream and recalc CRC
                            LocalRxBuf.SetLength(LocalRxBuf.Length - 4);
                            ushort calcCRC = CalcCRC_CITT(LocalRxBuf);

                            if (calcCRC == rcvCRC)
                            {
                                LocalRxBuf.Position = 1;
                                RxFrame.Address = MeComVarConvert.ReadUint8(LocalRxBuf);
                                RxFrame.SeqNr = MeComVarConvert.ReadUint16(LocalRxBuf);
                                RxFrame.Payload = new MemoryStream();
                                LocalRxBuf.CopyTo(RxFrame.Payload);
                                RxFrame.Payload.Position = 0; //Reset position for the user
                                RxFrame.RcvType = ERcvType.Data;
                                statistics.IncRxFrames();
                            }
                            else
                            {
                                statistics.IncCrcErrors();
                            }
                        }
                    }
                    else
                    {
                        LocalRxBuf?.WriteByte(c);
                    }
                }
            }
            catch (ArgumentOutOfRangeException)
            {
                //Just ignore. They are thrown from MeComVarConvert
            }
           
        }

        private ushort CalcCRC_CITT(MemoryStream Stream)
        {
            Stream.Position = 0;
            ushort CRC = 0;

            for (int i = 0; i < Stream.Length; i++)
            {
                CRC = CalcCRC_CITT(CRC, (byte)Stream.ReadByte());
            }
            return CRC;
        }

        private ushort CalcCRC_CITT(ushort n, byte m)
        {
            uint genPoly = 0x1021; //CCITT CRC-16 Polynomial
            uint uiCharShifted = ((uint)m & 0x00FF) << 8;
            n = (ushort)(n ^ uiCharShifted);
            for (uint i = 0; i < 8; i++)
            {
                if ((n & 0x8000) == 0x8000) n = (ushort)((n << 1) ^ genPoly);
                else n = (ushort)(n << 1);
            }
            return n;
        }
    }

    /// <summary>
    /// Represents all fields within an package.
    /// </summary>
    public struct MeComPacket
    {
        /// <summary>
        /// Initializes a new instance of an data package.
        /// </summary>
        /// <param name="control">The identifiers have been selected such that the receiving device, in order to detect the start of a frame, can synchronize to a character with a value.</param>
        /// <param name="address">Destination address.</param>
        public MeComPacket(char control, byte? address)
        {
            Control = control;
            Address = address;
            SeqNr = 0;
            Payload = new MemoryStream();
            RcvType = ERcvType.Empty;
        }

        /// <summary>
        /// The identifiers have been selected such that the receiving device, in order to detect the start of a frame, can synchronize to a character with a value.
        /// </summary>
        public char Control;

        /// <summary>
        /// Destination address.
        /// </summary>
        public byte? Address;

        /// <summary>
        /// Sequence number of the package. Should be incremented for each package
        /// that represents a new query or set with new content.
        /// Resend packages should contain the same sequence number.
        /// </summary>
        internal ushort SeqNr;

        /// <summary>
        /// Contains the Payload of the package.
        /// </summary>
        public MemoryStream Payload;

        /// <summary>
        /// Only used in case of reception. 
        /// Defines the type of package that has been received.
        /// </summary>
        public ERcvType RcvType;

    }

    /// <summary>
    /// Defines the type of the received package.
    /// </summary>
    public enum ERcvType
    {
        /// <summary>
        /// No package has been received. 
        /// The stream does not contain any data.
        /// </summary>
        Empty,
        /// <summary>
        /// A acknowledge has been received. 
        /// </summary>
        ACK,
        /// <summary>
        /// Data or an server error has been received.
        /// </summary>
        Data
    }
}
