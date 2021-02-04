using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using static MeSoft.MeCom.Core.MeComQuerySet;
using MeSoft.Core.Diagnostics;
using System.Threading;

namespace MeSoft.MeCom.Core
{
    /// <summary>
    /// Two communication commands. Only newer devices support them.
    /// Please have a look at the device specific communication protocol document.
    /// </summary>
    public class MeComG2Cmd
    {
        MeComQuerySet meQuerySet;

        /// <summary>
        /// Delegate used to report back the progress of long running functions. 
        /// </summary>
        /// <param name="progress">Progress 0 - 100</param>
        public delegate void ProgressUpdateCallback(double progress);

        /// <summary>
        /// Initializes a new instance of MeComG2Cmd.
        /// </summary>
        /// <param name="meQuerySet">Reference to the communication interface.</param>
        public MeComG2Cmd(MeComQuerySet meQuerySet)
        {
            this.meQuerySet = meQuerySet;
        }

        /// <summary>
        /// Returns Meta data of the parameter.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <returns>Returned meta data object.</returns>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public ParMetaData GetMetaData(byte? address, UInt16 parameterId, byte instance)
        {
            ParMetaData parMetaData = new ParMetaData();
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?VM");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComPacket rxFrame = meQuerySet.Query(txFrame);

                parMetaData.Type = (MeParType)MeComVarConvert.ReadUint8(rxFrame.Payload);
                parMetaData.Flags = (MeParFlags)MeComVarConvert.ReadUint8(rxFrame.Payload);
                parMetaData.NrOfInst = MeComVarConvert.ReadUint8(rxFrame.Payload);
                parMetaData.MaxNrOfElements = MeComVarConvert.ReadUint32(rxFrame.Payload);

                switch (parMetaData.Type)
                {
                    case MeParType.FLOAT32:
                        parMetaData.Min = MeComVarConvert.ReadFloat32(rxFrame.Payload);
                        parMetaData.Max = MeComVarConvert.ReadFloat32(rxFrame.Payload);
                        parMetaData.Value = MeComVarConvert.ReadFloat32(rxFrame.Payload);
                        break;
                    case MeParType.INT32:
                        parMetaData.Min = MeComVarConvert.ReadInt32(rxFrame.Payload);
                        parMetaData.Max = MeComVarConvert.ReadInt32(rxFrame.Payload);
                        parMetaData.Value = MeComVarConvert.ReadInt32(rxFrame.Payload);
                        break;
                    case MeParType.DOUBLE64:
                        parMetaData.Min = MeComVarConvert.ReadDouble64(rxFrame.Payload);
                        parMetaData.Max = MeComVarConvert.ReadDouble64(rxFrame.Payload);
                        parMetaData.Value = MeComVarConvert.ReadDouble64(rxFrame.Payload);
                        break;
                    case MeParType.LATIN1:
                    case MeParType.BYTE:
                        parMetaData.Min = MeComVarConvert.ReadUint8(rxFrame.Payload);
                        parMetaData.Max = MeComVarConvert.ReadUint8(rxFrame.Payload);
                        parMetaData.Value = null;
                        break;
                    default:
                        throw new ArgumentOutOfRangeException("Unknown Type received. Received value: " + parMetaData.Type);
                }
                return parMetaData;
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get Meta Data failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Sets a FLOAT32, INT32 or DOUBLE64 value to the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="type">Specifies the type of the value to be set.</param>
        /// <param name="value">Value to be set. Make sure this value fits to the specified type.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void SetValue(byte? address, UInt16 parameterId, byte instance, MeParType type, dynamic value)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "VS");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);


                switch (type)
                {
                    case MeParType.FLOAT32:
                        MeComVarConvert.AddFloat32(txFrame.Payload, value);
                        break;
                    case MeParType.INT32:
                        MeComVarConvert.AddInt32(txFrame.Payload, value);
                        break;
                    case MeParType.DOUBLE64:
                        MeComVarConvert.AddDouble64(txFrame.Payload, value);
                        break;
                    default:
                        throw new ArgumentOutOfRangeException("Unknown Type. Received value: " + type);
                }

                meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Set Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Returns a FLOAT32, INT32 or DOUBLE64 value from the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="type">Specifies the type of the value to be read.</param>
        /// <returns>Returned value.</returns>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public dynamic GetValue(byte? address, UInt16 parameterId, byte instance, MeParType type)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?VR");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComPacket rxFrame = meQuerySet.Query(txFrame);

                switch (type)
                {
                    case MeParType.FLOAT32:
                        return MeComVarConvert.ReadFloat32(rxFrame.Payload);
                    case MeParType.INT32:
                        return MeComVarConvert.ReadInt32(rxFrame.Payload);
                    case MeParType.DOUBLE64:
                        return MeComVarConvert.ReadDouble64(rxFrame.Payload);
                    default:
                        throw new ArgumentOutOfRangeException("Unknown Type. Received value: " + type);
                }
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Reads a list of values from the device within one command.
        /// This is much more efficient than reading each value with an separate command. 
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="elements">List of parameter definitions to read from the device.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void BulkParRead(byte? address, List<BulkParElement> elements)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?VX");
                MeComVarConvert.AddUint8(txFrame.Payload, (byte)elements.Count);

                foreach (BulkParElement item in elements)
                {
                    MeComVarConvert.AddUint16(txFrame.Payload, item.ParameterId);
                    MeComVarConvert.AddUint8(txFrame.Payload, item.Instance);
                }
                MeComPacket rxFrame = meQuerySet.Query(txFrame);
                foreach (BulkParElement item in elements)
                {
                    switch (item.Type)
                    {
                        case MeParType.FLOAT32:
                            item.Value = MeComVarConvert.ReadFloat32(rxFrame.Payload);
                            break;
                        case MeParType.INT32:
                            item.Value = MeComVarConvert.ReadInt32(rxFrame.Payload);
                            break;
                        case MeParType.DOUBLE64:
                            item.Value = MeComVarConvert.ReadDouble64(rxFrame.Payload);
                            break;
                    }
                }
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Bulk Parameter read failed Detail: {0}", Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Definition to make bulk par reads. Use BulkParRead.
        /// </summary>
        public class BulkParElement
        {
            /// <summary>Device Parameter ID.</summary>
            public UInt16 ParameterId;
            /// <summary> Parameter Instance. (usually 1) </summary>
            public byte Instance;
            /// <summary> Specifies the type of the value to be read. </summary>
            public MeParType Type;
            /// <summary> Will contain the read value. </summary>
            public dynamic Value;
            /// <summary> This value is not used by the BulkParRead. It may be used after reading the parameters to evaluate the result by the end user code. </summary>
            public object Parent;

            /// <summary>
            /// Initializes a new instance of BulkParElement.
            /// </summary>
            /// <param name="parameterId">Device Parameter ID.</param>
            /// <param name="instance">Specifies the type of the value to be read.</param>
            /// <param name="type">Will contain the read value.</param>
            /// <param name="parent">This value is not used by the BulkParRead.
            /// It may be used after reading the parameters to evaluate the result by the end user code.</param>
            public BulkParElement(UInt16 parameterId, byte instance, MeParType type, object parent = null)
            {
                ParameterId = parameterId;
                Instance = instance;
                Type = type;
                Parent = parent;
            }
        }

        /// <summary>
        /// Reads an array of FLOAT32, INT32, DOUBLE64 or ASCII (char) values form the device. 
        /// The data length is given by the device. 
        /// This method does only return when the device tells the host, that all data is read. 
        /// The data is read in an loop with several sub queries.
        /// During this command is working, it is possible to use other commands with an different thread.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="type">Specifies the type of the value to be read.</param>
        /// <param name="callback">Is called every time when the progress has changed.</param>
        /// <param name="expectedNrOfElements">Defines the expected number of elements to calculate the progress for the callback function.</param>
        /// <returns>Returned value.</returns>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public dynamic GetBigData(byte? address, UInt16 parameterId, byte instance, MeParType type, ProgressUpdateCallback callback = null, int expectedNrOfElements = 0)
        {
            dynamic value;
            try
            {
                ushort rcvElements;
                bool hasMoreData;
                uint totalReadElements = 0;
                MemoryStream totalStream = new MemoryStream();

                do
                {
                    MeComPacket txFrame = new MeComPacket('#', address);
                    MeComVarConvert.AddString(txFrame.Payload, "?VB");
                    MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                    MeComVarConvert.AddUint8(txFrame.Payload, instance);
                    MeComVarConvert.AddUint32(txFrame.Payload, totalReadElements); //Read start position
                    MeComVarConvert.AddUint16(txFrame.Payload, UInt16.MaxValue); //Maximum Elements to read per call.

                    MeComPacket rxFrame = meQuerySet.Query(txFrame);
                    rcvElements = MeComVarConvert.ReadUint16(rxFrame.Payload);
                    hasMoreData = MeComVarConvert.ReadUint8(rxFrame.Payload) == 1;
                    totalReadElements += rcvElements;
                    if (rcvElements > 0)
                    {
                        rxFrame.Payload.CopyTo(totalStream);
                    }

                    callback?.Invoke(100.0 / expectedNrOfElements * totalReadElements);

                } while (hasMoreData);

                totalStream.Position = 0;

                callback?.Invoke(100);

                switch (type)
                {
                    case MeParType.FLOAT32:
                        value = new float[totalReadElements];
                        break;
                    case MeParType.INT32:
                        value = new int[totalReadElements];
                        break;
                    case MeParType.DOUBLE64:
                        value = new double[totalReadElements];
                        break;
                    case MeParType.LATIN1:
                        value = "";
                        break;
                    case MeParType.BYTE:
                        value = new byte[totalReadElements];
                        break;
                    default:
                        throw new ArgumentOutOfRangeException("Unknown EParType: " + type);
                }

                for (int i = 0; i < totalReadElements; i++)
                {
                    switch (type)
                    {
                        case MeParType.FLOAT32:
                            value[i] = MeComVarConvert.ReadFloat32(totalStream);
                            break;
                        case MeParType.INT32:
                            value[i] = MeComVarConvert.ReadInt32(totalStream);
                            break;
                        case MeParType.DOUBLE64:
                            value[i] = MeComVarConvert.ReadDouble64(totalStream);
                            break;
                        case MeParType.LATIN1:
                            value = MeComVarConvert.ReadEncodedString(totalStream, (int)totalReadElements);
                            return value;
                        case MeParType.BYTE:
                            value[i] = MeComVarConvert.ReadUint8(totalStream);
                            break;
                        default:
                            throw new ArgumentOutOfRangeException("Unknown EParType: " + type);
                    }

                }
                return value;
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Writes an array of FLOAT32, INT32, DOUBLE64 or ASCII (char) values to the device. 
        /// The data length is given by the value parameter. 
        /// This method does only return when all data is downloaded. 
        /// The data is being written in a loop with several sub queries.
        /// While this command is working, it is possible to use other commands with a different thread.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="type">Specifies the type of the value to be written.</param>
        /// <param name="values">Data to be written (can be float[], int[], double[] or string.</param>
        /// <param name="callback">Is called every time when the progress has changed.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void SetBigData(byte? address, UInt16 parameterId, byte instance, MeParType type, dynamic values, ProgressUpdateCallback callback = null)
        {
            int maxDataSize = meQuerySet.MaxTxPayloadSize - 22; //-xx Bytes used for commands
            int nrOfElementsPerPackage;

            switch (type)
            {
                case MeParType.FLOAT32:
                    nrOfElementsPerPackage = maxDataSize / 8;
                    break;
                case MeParType.INT32:
                    nrOfElementsPerPackage = maxDataSize / 8;
                    break;
                case MeParType.DOUBLE64:
                    nrOfElementsPerPackage = maxDataSize / 16;
                    break;
                case MeParType.LATIN1:
                    values += (char)0; //Add zero terminator
                    nrOfElementsPerPackage = maxDataSize / 2;
                    break;
                case MeParType.BYTE:
                    nrOfElementsPerPackage = maxDataSize / 2;
                    break;
                default:
                    throw new ArgumentOutOfRangeException("Unknown EParType: " + type);
            }
            int nrOfPackages = (values.Length - 1) / nrOfElementsPerPackage + 1;

            try
            {
                int totalSentElements = 0;

                for (int packageNr = 0; packageNr < nrOfPackages; packageNr++)
                {
                    bool lastPackage = (packageNr + 1) == nrOfPackages;
                    int nrOfElementsInThisPackage = values.Length - totalSentElements;
                    if (nrOfElementsInThisPackage > nrOfElementsPerPackage) nrOfElementsInThisPackage = nrOfElementsPerPackage;

                    MeComPacket txFrame = new MeComPacket('#', address);
                    MeComVarConvert.AddString(txFrame.Payload, "VB");
                    MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                    MeComVarConvert.AddUint8(txFrame.Payload, instance);
                    MeComVarConvert.AddUint32(txFrame.Payload, (uint)totalSentElements); //write start position
                    MeComVarConvert.AddUint16(txFrame.Payload, (ushort)nrOfElementsInThisPackage);
                    if (lastPackage) MeComVarConvert.AddUint8(txFrame.Payload, 1); else MeComVarConvert.AddUint8(txFrame.Payload, 0);

                    switch (type)
                    {
                        case MeParType.FLOAT32:
                            for (int i = 0; i < nrOfElementsInThisPackage; i++) MeComVarConvert.AddFloat32(txFrame.Payload, values[totalSentElements + i]);
                            break;
                        case MeParType.INT32:
                            for (int i = 0; i < nrOfElementsInThisPackage; i++) MeComVarConvert.AddUint32(txFrame.Payload, values[totalSentElements + i]);
                            break;
                        case MeParType.DOUBLE64:
                            for (int i = 0; i < nrOfElementsInThisPackage; i++) MeComVarConvert.AddDouble64(txFrame.Payload, values[totalSentElements + i]);
                            break;
                        case MeParType.LATIN1:
                            MeComVarConvert.AddEncodedString(txFrame.Payload, values.Substring(totalSentElements, nrOfElementsInThisPackage));
                            break;
                        case MeParType.BYTE:
                            for (int i = 0; i < nrOfElementsInThisPackage; i++) MeComVarConvert.AddUint8(txFrame.Payload, values[totalSentElements + i]);
                            break;
                    }
                    int timeout = 0;
                    while (timeout < 50) //Manage device busy
                    {
                        timeout++;
                        try
                        {
                            meQuerySet.Set(txFrame);
                            break;
                        }
                        catch (ServerException ex)
                        {
                            if (ex.ServerErrorCode != 2) throw;
                            TraceLog.Verbose("Device busy detected. Timeout {0}", timeout);
                            Thread.Sleep(10);
                        }
                    }

                    totalSentElements += nrOfElementsInThisPackage;
                    callback?.Invoke(100.0 / nrOfPackages * (packageNr + 1));
                }
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Set Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Downloads a portion of a meerstetter firmware update file (*.mefw) to the device.
        /// This method must be called several times to download the whole content of the file.
        /// This method converts the data base64url and sends it.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="buffer">Portion of *.mefw file.</param>
        /// <param name="length">Length of the portion to download.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void DownloadFirmwareData(byte? address, byte[] buffer, int length)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "BS");
                MeComVarConvert.AddBase64url(txFrame.Payload, buffer, length);
                meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("DownloadFirmwareData failed: Address: {0}; Detail: {1}", address, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Enumeration of the available parameter system types.
        /// </summary>
        public enum MeParType
        {
            /// <summary>float value.</summary>
            FLOAT32 = 0,
            /// <summary>signed int value.</summary>
            INT32 = 1,
            /// <summary>double value.</summary>
            DOUBLE64 = 2,
            /// <summary>Latin-1 string according to ISO-8859-1 (like standard ASCII). On .net side this type is represented as normal string.</summary>
            LATIN1 = 3,
            /// <summary>Byte Array. C: unsigned char. C#: byte</summary>
            BYTE = 4,
        }

        /// <summary>
        /// Returns the byte length of the type.
        /// </summary>
        /// <param name="Type">Value Type.</param>
        /// <returns>length of the given type.</returns>
        public byte GetTypeLength(MeParType Type)
        {
            switch (Type)
            {
                case MeParType.FLOAT32:
                    return 4;
                case MeParType.INT32:
                    return 4;
                case MeParType.DOUBLE64:
                    return 8;
                case MeParType.LATIN1:
                    return 1;
                default:
                    throw new ArgumentOutOfRangeException("Get Type Length: Unknown EParType: " + Type);
            }
        }

        /// <summary>
        /// Meta Data Flags for parameters.
        /// </summary>
        [Flags]
        public enum MeParFlags
        {
            /// <summary>Reading of the value is allowed.</summary>
            ReadOK = 1,
            /// <summary>Writing of the value is allowed.</summary>
            WriteOK = 2
        }

        /// <summary>
        /// Parameter Meta Data definition.
        /// </summary>
        public class ParMetaData
        {
            /// <summary>Parameter value type.</summary>
            public MeParType Type;
            /// <summary>Parameter value flags.</summary>
            public MeParFlags Flags;
            /// <summary>Number of instances available on this parameter.</summary>
            public byte NrOfInst;
            /// <summary>Maximum number of elements available on this parameter (usually 1).</summary>
            public UInt32 MaxNrOfElements;
            /// <summary>Minimal allowed value of the parameter.</summary>
            public dynamic Min;
            /// <summary>Maximal allowed value of the parameter.</summary>
            public dynamic Max;
            /// <summary>Current parameter value.</summary>
            public dynamic Value;
        }
    }
}
