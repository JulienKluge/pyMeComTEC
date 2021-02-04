using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace MeSoft.MeCom.Core
{
    /// <summary>
    /// Contains functions format or interpret communication strings. 
    /// </summary>
    public static class MeComVarConvert
    {
        #region Add functions

        /// <summary> Encodes the byte array base64url and adds it to the stream. </summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="array">Data source.</param>
        /// <param name="length">Length of data source.</param>
        public static void AddBase64url(MemoryStream stream, byte[] array, int length)
        {
            string base64String = Convert.ToBase64String(array, 0, length);
            base64String = base64String.Replace('+', '-');
            base64String = base64String.Replace('/', '_');
            BinaryWriter binaryWriter = new BinaryWriter(stream);
            binaryWriter.Write(base64String.ToCharArray());
        }

        /// <summary> Writes a string to the stream.  </summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddString(MemoryStream stream, string value)
        {
            char[] cArray = value.ToCharArray();

            for (int i = 0; i < cArray.Length; i++)
            {
                stream.WriteByte(Convert.ToByte(cArray[i]));
            }
        }

        /// <summary>Writes a UINT4 (byte range 0-15) to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddUint4(MemoryStream stream, Byte value)
        {
            stream.WriteByte(ConvertToHex((value >> 0) & 0xF));
        }

        /// <summary>Writes a INT8 (signed byte) to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddInt8(MemoryStream stream, SByte value)
        {
            AddUint8(stream, (byte)value);
        }

        /// <summary>Writes a UINT8 (unsigned byte) to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddUint8(MemoryStream stream, Byte value)
        {
            stream.WriteByte(ConvertToHex((value >> 4) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 0) & 0xF));
        }

        /// <summary>Writes a INT16 to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddInt16(MemoryStream stream, Int16 value)
        {
            AddUint16(stream, (UInt16)value);
        }

        /// <summary>Writes a UINT16 to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddUint16(MemoryStream stream, UInt16 value)
        {
            stream.WriteByte(ConvertToHex((value >> 12) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 8) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 4) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 0) & 0xF));
        }

        /// <summary>Writes a INT32 to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddInt32(MemoryStream stream, Int32 value)
        {
            AddUint32(stream, (UInt32)value);
        }

        /// <summary>Writes a FLOAT32 (.net float) to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddFloat32(MemoryStream stream, float value)
        {
            UInt32 x = BitConverter.ToUInt32(BitConverter.GetBytes(value), 0);
            AddUint32(stream, x);
        }

        /// <summary>Writes a UINT32 to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddUint32(MemoryStream stream, UInt32 value)
        {
            stream.WriteByte(ConvertToHex((value >> 28) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 24) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 20) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 16) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 12) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 8) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 4) & 0xF));
            stream.WriteByte(ConvertToHex((value >> 0) & 0xF));
        }

        /// <summary>Writes a DOUBLE64 (.net double) to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddDouble64(MemoryStream stream, double value)
        {
            UInt64 x = BitConverter.ToUInt64(BitConverter.GetBytes(value), 0);
            AddUint64(stream, x);
        }

        /// <summary>Writes a UINT64 to the stream.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        static void AddUint64(MemoryStream stream, UInt64 value)
        {
            stream.WriteByte(ConvertToHex((Int64)((value >> 60) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 56) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 52) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 48) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 44) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 40) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 36) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 32) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 28) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 24) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 20) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 16) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 12) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 8) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 4) & 0xF)));
            stream.WriteByte(ConvertToHex((Int64)((value >> 0) & 0xF)));
        }

        /// <summary>Adds the string to the stream payload. The string is converted to an ASCII char array. 
        /// Then each ASCII char is added as a UINT8 element to the stream. Therefore the whole ASCII range can be used.
        /// If a zero terminator is needed, just add it to the string before you run this method.</summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddEncodedString(MemoryStream stream, string value)
        {
            byte[] asciiByteArray = Encoding.GetEncoding("ISO-8859-1").GetBytes(value);
            foreach (byte item in asciiByteArray) AddUint8(stream, item);
        }

        /// <summary>
        /// Writes each byte in the array to the stream.
        /// </summary>
        /// <param name="stream">Writes data to this stream.</param>
        /// <param name="value">Value to be added.</param>
        public static void AddByteArray(MemoryStream stream, byte[] value)
        {
            foreach (byte item in value) AddUint8(stream, item);
        }

        /// <summary>Converts a value from 0 - 15 to a char '0' - 'F'</summary>
        /// <param name="value">Number value to be converted.</param>
        /// <returns>char value '0' - 'F' represented by a byte value.</returns>
        /// <exception cref="ArgumentOutOfRangeException">if value is not 0-15.</exception>
        public static byte ConvertToHex(Int64 value)
        {
            switch (value)
            {
                case 0: return Convert.ToByte('0');
                case 1: return Convert.ToByte('1');
                case 2: return Convert.ToByte('2');
                case 3: return Convert.ToByte('3');
                case 4: return Convert.ToByte('4');
                case 5: return Convert.ToByte('5');
                case 6: return Convert.ToByte('6');
                case 7: return Convert.ToByte('7');
                case 8: return Convert.ToByte('8');
                case 9: return Convert.ToByte('9');
                case 10: return Convert.ToByte('A');
                case 11: return Convert.ToByte('B');
                case 12: return Convert.ToByte('C');
                case 13: return Convert.ToByte('D');
                case 14: return Convert.ToByte('E');
                case 15: return Convert.ToByte('F');

                default:
                    throw new ArgumentOutOfRangeException();
            }
        }

        #endregion 

        #region Read functions

        /// <summary>
        /// Reads a string with an specified length from the stream. 
        /// The chars are not encoded, therefore only a limited range of chars are allowed.
        /// Basically 'A-Z', 'a-z', '0-9', '-', ' ', 
        /// For example, carriage return or line feed are not allowed, 
        /// because they would conflict the communication protocol 'control characters'.
        /// </summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <param name="Length">Length of the read string. To read 20 chars, write 20 to this parameter.</param>
        /// <returns>The read and converted value.</returns>
        public static string ReadString(MemoryStream Stream, int Length)
        {
            byte[] byteStr = new byte[Length];
            Stream.Read(byteStr, 0, Length);
            return System.Text.Encoding.ASCII.GetString(byteStr);
        }

        /// <summary>
        /// Reads a 0 terminated string from the stream. Each char is read as UINT8 element.
        /// Therefore the full ASCII range is usable.
        /// Stops writing to the output when 0 is detected.
        /// Reads always readNrOfElements from the stream.
        /// </summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <param name="readNrOfElements">Number of elements to be read from the stream. In this case 1 element equals 2 bytes.</param>
        /// <returns>The read and converted value.</returns>
        public static string ReadEncodedString(MemoryStream Stream, int readNrOfElements)
        {
            bool endDetected = false;
            int bytesToConvert = 0;
            byte[] byteStr = new byte[readNrOfElements];
            for (int i = 0; i < readNrOfElements; i++)
            {
                byte read = ReadUint8(Stream);
                if (read == 0 || endDetected) //Stop if a 0 is detected, but read out the full buffer
                {
                    endDetected = true;
                }
                else
                {
                    byteStr[i] = read;
                    bytesToConvert = i + 1;
                }
            }

            return System.Text.Encoding.GetEncoding("ISO-8859-1").GetString(byteStr, 0, bytesToConvert);
        }

        /// <summary>Reads a UINT4 (byte range 0-15) from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static Byte ReadUint4(MemoryStream Stream)
        {
            Int64 value = (ConvertToNr(Stream.ReadByte()) << 0);

            return (Byte)value;
        }

        /// <summary>Reads a UINT8 (byte) from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static Byte ReadUint8(MemoryStream Stream)
        {
            Int64 value =
                (ConvertToNr(Stream.ReadByte()) << 4) +
                (ConvertToNr(Stream.ReadByte()) << 0);

            return (Byte)value;
        }

        /// <summary>Reads a UINT16 from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static Int16 ReadInt16(MemoryStream Stream)
        {
            return (Int16)ReadUint16(Stream);
        }

        /// <summary>Reads a UINT16 from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static UInt16 ReadUint16(MemoryStream Stream)
        {
            Int64 value =
                (ConvertToNr(Stream.ReadByte()) << 12) +
                (ConvertToNr(Stream.ReadByte()) << 8) +
                (ConvertToNr(Stream.ReadByte()) << 4) +
                (ConvertToNr(Stream.ReadByte()) << 0);

            return (UInt16)value;
        }

        /// <summary>Reads a INT32 from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static Int32 ReadInt32(MemoryStream Stream)
        {
            return (Int32)ReadUint32(Stream);
        }

        /// <summary>Reads a FLOAT32 (.net float) from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static float ReadFloat32(MemoryStream Stream)
        {
            return BitConverter.ToSingle(BitConverter.GetBytes(ReadUint32(Stream)), 0);
        }

        /// <summary>Reads a DOUBLE64 (.net double) from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static double ReadDouble64(MemoryStream Stream)
        {
            return BitConverter.ToDouble(BitConverter.GetBytes(ReadUint64(Stream)), 0);
        }

        /// <summary>Reads a UINT32 from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        public static UInt32 ReadUint32(MemoryStream Stream)
        {
            Int64 value =
                (ConvertToNr(Stream.ReadByte()) << 28) +
                (ConvertToNr(Stream.ReadByte()) << 24) +
                (ConvertToNr(Stream.ReadByte()) << 20) +
                (ConvertToNr(Stream.ReadByte()) << 16) +
                (ConvertToNr(Stream.ReadByte()) << 12) +
                (ConvertToNr(Stream.ReadByte()) << 8) +
                (ConvertToNr(Stream.ReadByte()) << 4) +
                (ConvertToNr(Stream.ReadByte()) << 0);

            return (UInt32)value;
        }

        /// <summary>Reads a UINT64 from the stream.</summary>
        /// <param name="Stream">Stream where the value is read from.</param>
        /// <returns>The read and converted value.</returns>
        static UInt64 ReadUint64(MemoryStream Stream)
        {
            Int64 value =
                (ConvertToNr(Stream.ReadByte()) << 60) +
                (ConvertToNr(Stream.ReadByte()) << 56) +
                (ConvertToNr(Stream.ReadByte()) << 52) +
                (ConvertToNr(Stream.ReadByte()) << 48) +
                (ConvertToNr(Stream.ReadByte()) << 44) +
                (ConvertToNr(Stream.ReadByte()) << 40) +
                (ConvertToNr(Stream.ReadByte()) << 36) +
                (ConvertToNr(Stream.ReadByte()) << 32) +
                (ConvertToNr(Stream.ReadByte()) << 28) +
                (ConvertToNr(Stream.ReadByte()) << 24) +
                (ConvertToNr(Stream.ReadByte()) << 20) +
                (ConvertToNr(Stream.ReadByte()) << 16) +
                (ConvertToNr(Stream.ReadByte()) << 12) +
                (ConvertToNr(Stream.ReadByte()) << 8) +
                (ConvertToNr(Stream.ReadByte()) << 4) +
                (ConvertToNr(Stream.ReadByte()) << 0);

            return (UInt64)value;
        }

        /// <summary>Converts a char from '0' - 'F' to a number value 0-15.</summary>
        /// <param name="value">char value '0' - 'F' represented by a int.</param>
        /// <returns>number value 0-15.</returns>
        /// <exception cref="ArgumentOutOfRangeException">if char value is not '0' - '15'.</exception>
        public static Int64 ConvertToNr(int value)
        {
            switch (value)
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

                default:
                    throw new ArgumentOutOfRangeException();
            }
        }

        #endregion


    }
}
