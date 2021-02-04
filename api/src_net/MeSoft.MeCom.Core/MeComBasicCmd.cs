using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using MeSoft.MeCom.Core;

namespace MeSoft.MeCom.Core
{
    /// <summary>
    /// Basic communication commands. Most of the products do support them.
    /// </summary>
    public class MeComBasicCmd
    {
        MeComQuerySet meQuerySet;

        /// <summary>
        /// Initializes a new instance of MeComBasicCmd.
        /// </summary>
        /// <param name="meQuerySet">Reference to the communication interface.</param>
        public MeComBasicCmd(MeComQuerySet meQuerySet)
        {
            this.meQuerySet = meQuerySet;
        }

        #region Misc Functions

        /// <summary>
        /// Resets the device. 
        /// Usually the device does answer to this command, because the reset is slightly delayed.
        /// During reboot, the device can not answer to commands.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void ResetDevice(byte? address)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "RS");
                meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Reset Device failed: Address: {0}, Detail: {1}", address, Ex.Message), Ex);
            }
              
        }

        /// <summary>
        /// Returns the Device Identification String.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <returns>Device Identification String. Usually 20 Chars long.</returns>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public string GetIdentString(byte? address)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?IF");
                MeComPacket rxFrame = meQuerySet.Query(txFrame);
                return MeComVarConvert.ReadString(rxFrame.Payload, 20);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get Identification String failed: Address: {0}, Detail: {1}", address, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Changes the baud rate of the device on the interface where this command is being received.
        /// Do not forget to change the host baud rate after this command (MeComSetDefaultSettings).
        /// Most devices will fall back to the old baud rate if there is no further command being received after CS within 5s.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="newBaudRate">New baud rate to be set on the devices interface.</param>
        public void ChangeComSpeed(byte? address, uint newBaudRate)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "CS");
                MeComVarConvert.AddUint32(txFrame.Payload, newBaudRate);
                MeComPacket RxFrame = meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Speed Change failed: Address: {0}, Detail: {1}", address, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Queries the Branch ID. 
        /// The Branch ID can be used to identify several software branches from the same software.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <returns>Branch ID</returns>
        public int GetBranchId(byte? address)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?BI");
                MeComPacket rxFrame = meQuerySet.Query(txFrame);
                return MeComVarConvert.ReadInt32(rxFrame.Payload);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get Branch ID failed: Address: {0}; Detail: {1}", address, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Can download the file content of the Settings Dump file (*.mepar), which is created using the TEC Service Software. 
        /// See Maintenance tab. 
        /// Please read the TEC User Manual for further information about this feature. 
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="fileContent">Content of the .mepar file.</param>
        public void DownloadSettingsDumpFile(byte? address, string fileContent)
        {
            string[] settingsStrings = fileContent.Split(new string[] { "\r\n" }, StringSplitOptions.RemoveEmptyEntries);

            if (settingsStrings.Length == 0)
            {
                throw new FormatException("The fileContent does not contain any settings strings!");
            }

            try
            {
                foreach (string settingsString in settingsStrings)
                {
                    MeComPacket txFrame = new MeComPacket('#', address);
                    MeComVarConvert.AddString(txFrame.Payload, "?SD");
                    MeComVarConvert.AddString(txFrame.Payload, settingsString);
                    MeComPacket rxFrame = meQuerySet.Query(txFrame);
                    if (MeComVarConvert.ReadUint4(rxFrame.Payload) != 0)
                    {
                        throw new InvalidOperationException("The settings string has not been accepted (CRC error)!");
                    }
                }
            }
            catch (Exception ex)
            {
                throw new ComCommandException(String.Format("Download Settings File failed: Address: {0}, Detail: {1}", address, ex.Message), ex);
            }
        }

        #endregion


        #region Functions for ID Parameter system
        /// <summary>
        /// Returns a signed int 32Bit value from the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <returns>Returned value.</returns>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public int GetINT32Value(byte? address, UInt16 parameterId, byte instance)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?VR");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComPacket rxFrame = meQuerySet.Query(txFrame);
                return MeComVarConvert.ReadInt32(rxFrame.Payload);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get INT32 Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }
        /// <summary>
        /// Returns a float 32Bit value from the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <returns>Returned value.</returns>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public float GetFloatValue(byte? address, UInt16 parameterId, byte instance)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?VR");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComPacket rxFrame = meQuerySet.Query(txFrame);
                return MeComVarConvert.ReadFloat32(rxFrame.Payload);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get FLOAT Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Returns a double 64Bit value from the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <returns>Returned value.</returns>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public double GetDoubleValue(byte? address, UInt16 parameterId, byte instance)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?VR");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComPacket rxFrame = meQuerySet.Query(txFrame);
                return MeComVarConvert.ReadDouble64(rxFrame.Payload);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get Double Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Sets a signed int 32Bit value to the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="value">Value to set.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void SetINT32Value(byte? address, UInt16 parameterId, byte instance, int value)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "VS");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComVarConvert.AddInt32(txFrame.Payload, value);
                meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Set INT32 Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Sends out a command to set the device address by type and serial number
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="deviceType">Type of the device.</param>
        /// <param name="serialNumber">Serial number of the Device</param>
        /// <param name="setaddress">Address to be set.</param>
        /// <param name="option">Option. 0=Set address, 1=rack system.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void SetDeviceAddress(byte? address, int deviceType, int serialNumber, byte setaddress, byte option)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "SA");
                MeComVarConvert.AddInt32(txFrame.Payload, deviceType);
                MeComVarConvert.AddInt32(txFrame.Payload, serialNumber);
                MeComVarConvert.AddUint8(txFrame.Payload, option);
                MeComVarConvert.AddUint8(txFrame.Payload, setaddress);
                meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Set Device Address failed: Address: {0}; Device Type: {1}; Serial Number: {2}; Address to be set: {3}", deviceType, serialNumber, setaddress, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Sets a float 32Bit value to the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="value">Value to set.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void SetFloatValue(byte? address, UInt16 parameterId, byte instance, float value)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "VS");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComVarConvert.AddFloat32(txFrame.Payload, value);
                meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Set FLOAT Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }
        /// <summary>
        /// Sets a double 64Bit value to the device.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="value">Value to set.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void SetDoubleValue(byte? address, UInt16 parameterId, byte instance, double value)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "VS");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComVarConvert.AddDouble64(txFrame.Payload, value);
                meQuerySet.Set(txFrame);
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Set Double Value failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }

        /// <summary>
        /// Returns the basic Meta data to the parameter.
        /// </summary>
        /// <param name="address">Device Address. Use null to use the DefaultDeviceAddress defined on MeComQuerySet.</param>
        /// <param name="parameterId">Device Parameter ID.</param>
        /// <param name="instance">Parameter Instance. (usually 1)</param>
        /// <param name="min">Minimal value. Is always a double value.</param>
        /// <param name="max">Maximal value. Is always a double value.</param>
        /// <exception cref="ComCommandException">when the command fails. Check the inner exception for details.</exception>
        public void GetLimits(byte? address, ushort parameterId, byte instance, out double min, out double max)
        {
            try
            {
                MeComPacket txFrame = new MeComPacket('#', address);
                MeComVarConvert.AddString(txFrame.Payload, "?VL");
                MeComVarConvert.AddUint16(txFrame.Payload, parameterId);
                MeComVarConvert.AddUint8(txFrame.Payload, instance);
                MeComPacket rxFrame = meQuerySet.Query(txFrame);
                if (MeComVarConvert.ReadUint8(rxFrame.Payload) == 0)
                {
                    //This is a float Value
                    min = MeComVarConvert.ReadFloat32(rxFrame.Payload);
                    max = MeComVarConvert.ReadFloat32(rxFrame.Payload);
                }
                else
                {
                    //This is a INT32 Value
                    min = MeComVarConvert.ReadInt32(rxFrame.Payload);
                    max = MeComVarConvert.ReadInt32(rxFrame.Payload);
                }
            }
            catch (Exception Ex)
            {
                throw new ComCommandException(String.Format("Get Limit Values failed: Address: {0}; ID: {1}; Inst: {2}; Detail: {3}", address, parameterId, instance, Ex.Message), Ex);
            }
        }
        #endregion
    }
}
