using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using MeSoft.MeCom.PhyWrapper;
using System.Threading;
using MeSoft.Core.Diagnostics;

namespace MeSoft.MeCom.Core
{
    /// <summary>
    /// Represents the transport layer of the communication protocol.
    /// Is responsible that each query of set is executed correctly, 
    /// otherwise it will throw an exception.
    /// </summary>
    public class MeComQuerySet
    {
        #region Public Values for upper layer convenience 

        /// <summary>
        /// true when the interface is ready to use; false if not. 
        /// </summary>
        /// <remarks>
        /// Is automatically set to false if an interface error or timeout error occurs. 
        /// Must be set from application level with SetIsReady() function.
        /// </remarks>
        public bool IsReady
        {
            get { return isReady; }
            private set 
            {
                if (value == false) VersionIsOK = false;
                isReady = value; 
            }
        }
        bool isReady;

        /// <summary>
        /// Used from application level to inform other threads that the interface is ready.
        /// </summary>
        /// <remarks>
        /// Usually the application device connector searches for a valid device
        /// and sets then the interface as ready.
        /// </remarks>
        /// <exception cref="NotSupportedException">
        /// Thrown when another thread than the creator of this instance tries to set ready.
        /// </exception>
        public void SetIsReady(bool isReady)
        {
            if (Thread.CurrentThread.ManagedThreadId != threadIdOfCreator && isReady == true)
                throw new NotSupportedException("Only the creator thread can set the ready status!");

            this.IsReady = isReady;
        }

        /// <summary>
        /// true when the application connector has recognized a valid device firmware version;
        /// </summary>
        /// <remarks>
        /// Is automatically set to false if an interface error or timeout error occurs. 
        /// Must be set from application level with SetVersionIsOK() function.
        /// </remarks>
        public bool VersionIsOK
        {
            get { return versionIsOK; }
            private set { versionIsOK = value; }
        }
        private bool versionIsOK;

        /// <summary>
        /// Used from application level to inform other threads that the interface 
        /// is connected to a device with an valid firmware version. 
        /// </summary>
        /// <exception cref="NotSupportedException">
        /// Thrown when another thread than the creator of this instance tries to set version OK.
        /// </exception>
        public void SetVersionIsOK(bool versionIsOK)
        {
            if (Thread.CurrentThread.ManagedThreadId != threadIdOfCreator)
                throw new NotSupportedException("Only the creator thread can set the VersionIsOK status!");

            this.VersionIsOK = versionIsOK;
        }

        /// <summary>
        /// Represents the default destination address for the device to be addressed.
        /// This value is used if null is passed for the device address in a package.
        /// </summary>
        /// <remarks>
        /// To set this value use the function SetDefaultDeviceAddress().
        /// </remarks>
        public byte DefaultDeviceAddress
        {
            get { return _DefaultDeviceAddress; }
            private set { _DefaultDeviceAddress = value; }
        }
        private byte _DefaultDeviceAddress;

        /// <summary>
        /// Sets the default destination address for the device to be addressed.
        /// This value is used if null is passed for the device address in a package.
        /// </summary>
        /// <remarks>
        /// Usually the application device connector searches for a valid device
        /// and sets then this value.
        /// </remarks>
        /// <exception cref="NotSupportedException">
        /// Thrown when another thread than the creator of this instance tries to set.
        /// </exception>
        public void SetDefaultDeviceAddress(byte address)
        {
            if (Thread.CurrentThread.ManagedThreadId != threadIdOfCreator)
            {
                throw new NotSupportedException("Only the creator thread can set the default device address!");
            }

            DefaultDeviceAddress = address;
        }

        /// <summary>
        /// Returns the collected communication statistics data.
        /// </summary>
        /// <param name="xmlTable">Table with all the values.</param>
        /// <param name="additionalText">Additional text to display.</param>
        public void GetStatistics(out string xmlTable, out string additionalText)
        {
            statistics.GetStatistics(out xmlTable, out additionalText);
        }

        /// <summary>
        /// Defines the maximum payload size in bytes that is sent over the underlying interface. 
        /// This value is not directly used by this class. (just a definition)
        /// It is intended to use by the higher levels to calculate the maximum allowed elements size. 
        /// For example where a query must be scaled into several sub queries.
        /// The default value is 1024 Bytes. 
        /// </summary>
        public int MaxTxPayloadSize { get; set; } = 1024;


        #endregion




        object lockObj = new object();
        int threadIdOfCreator;

        IMeComPhy phyCom;
        MeComFrame meFrame;
        UInt16 sequenceNr;
        Statistics statistics = new Statistics();
        
        /// <summary>
        /// Initializes the communication interface.
        /// This object can then be passed to the Command objects like MeBasicCmd.
        /// </summary>
        /// <param name="phyCom">Physical connection.</param>
        public MeComQuerySet(IMeComPhy phyCom)
        {
            this.phyCom = phyCom;
            meFrame = new MeComFrame(phyCom, statistics);

            Random rand = new Random();
            sequenceNr = Convert.ToUInt16(rand.Next(65535));

            threadIdOfCreator = Thread.CurrentThread.ManagedThreadId;
        }

        /// <summary>
        /// Executes a Query. A Query is used to get some data back from the server.
        /// It tries automatically 3 times to resend the package if no data is replayed from the server
        /// of if the returned data is wrong.
        /// </summary>
        /// <param name="txFrame">Definition of the data to send.</param>
        /// <returns>Received data.</returns>
        /// <exception cref="GeneralException">on timeout or any other exception. Check the inner exception for details.</exception>
        /// <exception cref="ServerException">when the server replays with an Server Error Code.</exception>
        /// <exception cref="NotConnectedException">when the interface is not connected. 
        /// (Only if the calling thread is different from the creator of this object)</exception>
        public MeComPacket Query(MeComPacket txFrame)
        {
            try
            {
                statistics.ThreadWaitForLock();
                CheckIfConnectedOrException();
                lock (lockObj)
                {
                    statistics.ThreadLockEntered();
                    CheckIfConnectedOrException();
                    try
                    {
                        return LocalQuery(txFrame);
                    }
                    catch (ServerException ex)
                    {
                        TraceLog.Warn("Thread '{0}': {1}", Thread.CurrentThread.Name, ex.Message);
                        throw;
                    }
                    catch(Exception ex)
                    {
                        TraceLog.Warn("Thread '{0}': {1}", Thread.CurrentThread.Name, ex.Message);
                        IsReady = false;
                        throw;
                    }
                }
            }
            finally
            {
                statistics.ThreadExited();
            }
        }

        /// <summary>
        /// Executes a Set. A Set is used to set some data to the server. 
        /// No data can be received from the server. 
        /// It tries automatically 3 times to resend the package if no data is replayed from the server
        /// of if the returned data is wrong.
        /// </summary>
        /// <param name="txFrame">Definition of the data to send.</param>
        /// <returns>Received data</returns>
        /// <exception cref="GeneralException">on timeout or any other exception. Check the inner exception for details.</exception>
        /// <exception cref="ServerException">when the server replays with an Server Error Code.</exception>
        /// <exception cref="NotConnectedException">when the interface is not connected. 
        /// (Only if the calling thread is different from the creator of this object)</exception>
        public MeComPacket Set(MeComPacket txFrame)
        {
            try
            {
                statistics.ThreadWaitForLock();
                CheckIfConnectedOrException();
                lock (lockObj)
                {
                    statistics.ThreadLockEntered();
                    CheckIfConnectedOrException();
                    try
                    {
                        return LocalSet(txFrame);
                    }
                    catch (ServerException ex)
                    {
                        TraceLog.Warn("Thread '{0}': {1}", Thread.CurrentThread.Name, ex.Message);
                        throw;
                    }
                    catch (Exception ex)
                    {
                        TraceLog.Warn("Thread '{0}': {1}", Thread.CurrentThread.Name, ex.Message);
                        IsReady = false;
                        throw;
                    }
                }
            }
            finally
            {
                statistics.ThreadExited();
            }
        }

        /// <summary>
        /// Changes the physical connection interface for this communication object.
        /// </summary>
        /// <param name="phyCom"></param>
        /// <exception cref="NotSupportedException">when a different thread then the creator of this object 
        /// tries to change the physical interface.</exception>
        public void ChangePhyCom(IMeComPhy phyCom)
        {
            lock (lockObj)
            {
                if (Thread.CurrentThread.ManagedThreadId != threadIdOfCreator)
                {
                    throw new NotSupportedException("Only the creator thread can change the physical interface!");
                }

                this.phyCom = phyCom;
                meFrame = new MeComFrame(this.phyCom, statistics);
            }
        }




        MeComPacket LocalQuery(MeComPacket txFrame)
        {
            if (txFrame.Address == null) txFrame.Address = DefaultDeviceAddress;

            sequenceNr++;
            int trialsLeft = 3;
            MeComPacket rxFrame = new MeComPacket();

            while (trialsLeft > 0)
            {
                trialsLeft--;
                txFrame.SeqNr = sequenceNr;
                
                try
                {
                    meFrame.SendFrame(txFrame);
                    if (txFrame.Address == 255) return rxFrame; //On the address 255, no answer is expected
                    rxFrame = meFrame.ReceiveFrameOrTimeout();
                    if (rxFrame.RcvType == ERcvType.Data && rxFrame.SeqNr == sequenceNr && rxFrame.Address == txFrame.Address)
                    {
                        //Corresponding Frame received
                        if (rxFrame.Payload.ReadByte() == '+')
                        {
                            SetServerErrorException(MeComVarConvert.ReadUint8(rxFrame.Payload));
                        }
                        else
                        {
                            rxFrame.Payload.Position = 0; //Set stream position to 0 for the user
                            return rxFrame;
                        }
                    }
                }
                catch (MeComPhyTimeoutException ex)
                {
                    //Ignore Timeout on this level if some trials are left
                    if (trialsLeft == 0) throw new GeneralException("Query failed: Timeout!", ex);
                    TraceLog.Info("Thread '{0}': Package re-send. NrOfTrails {1}", Thread.CurrentThread.Name, trialsLeft);
                }
                catch (ServerException)
                {
                    throw;
                }
                catch (Exception ex)
                {
                    throw new GeneralException("Query failed: " + ex.Message, ex);
                }
            }

            //Communication failed, check last error
            if (rxFrame.RcvType != ERcvType.Data) throw new GeneralException("Query failed: Wrong Type of package received. Received " + rxFrame.RcvType + "; Expected " + ERcvType.Data);
            if (rxFrame.SeqNr != sequenceNr) throw new GeneralException("Query failed: Wrong Sequence Number received. Received " + rxFrame.SeqNr + "; Expected " + sequenceNr);
            if (rxFrame.Address != txFrame.Address) throw new GeneralException("Query failed: Wrong Address received. Received " + rxFrame.Address + "; Expected " + txFrame.Address);

            throw new GeneralException("Query failed: Unknown error");
        }

        MeComPacket LocalSet(MeComPacket txFrame)
        {
            if (txFrame.Address == null) txFrame.Address = DefaultDeviceAddress;

            sequenceNr++;
            int trialsLeft = 3;
            MeComPacket rxFrame = new MeComPacket();

            while (trialsLeft > 0)
            {
                trialsLeft--;
                txFrame.SeqNr = sequenceNr;
                
                try
                {
                    meFrame.SendFrame(txFrame);
                    if (txFrame.Address == 255) return rxFrame; //On the address 255, no answer is expected
                    rxFrame = meFrame.ReceiveFrameOrTimeout();

                    if (rxFrame.SeqNr == sequenceNr && rxFrame.Address == txFrame.Address)
                    {
                        //Corresponding Frame received
                        if (rxFrame.RcvType == ERcvType.Data)
                        {
                            //Data Frame received --> Check for error code
                            if (rxFrame.Payload.ReadByte() == '+')
                            {
                                SetServerErrorException(MeComVarConvert.ReadUint8(rxFrame.Payload));
                            }
                            else
                            {
                                rxFrame.Payload.Position = 0; //Set stream position to 0 for the user
                                return rxFrame;
                            }
                        }
                        else if (rxFrame.RcvType == ERcvType.ACK)
                        {
                            return rxFrame;
                        }
                    }
                }
                catch (MeComPhyTimeoutException Ex)
                {
                    //Ignore Timeout on this level if some trials are left
                    if (trialsLeft == 0) throw new GeneralException("Set failed: Timeout!", Ex);
                    TraceLog.Info("Thread '{0}': Package re-send. NrOfTrails {1}", Thread.CurrentThread.Name, trialsLeft);
                }
                catch (ServerException)
                {
                    throw;
                }
                catch (Exception Ex)
                {
                    throw new GeneralException("Set failed: " + Ex.Message, Ex);
                }
            }

            //Communication failed, check last error
            if (rxFrame.SeqNr != sequenceNr) throw new GeneralException("Set failed: Wrong Sequence Number received. Received " + rxFrame.SeqNr + "; Expected " + sequenceNr);
            if (rxFrame.Address != txFrame.Address) throw new GeneralException("Set failed: Wrong Address received. Received " + rxFrame.Address + "; Expected " + txFrame.Address);

            throw new GeneralException("Set failed: Unknown error");
        }

        void SetServerErrorException(int ErrorCode)
        {
            string serverErrorMessage;
            switch (ErrorCode)
            {
                case 1:
                    serverErrorMessage = "Command not available";
                    break;
                case 2:
                    serverErrorMessage = "Device is busy";
                    break;
                case 3:
                    serverErrorMessage = "General communication error";
                    break;
                case 4:
                    serverErrorMessage = "Format error";
                    break;
                case 5:
                    serverErrorMessage = "Parameter is not available";
                    break;
                case 6:
                    serverErrorMessage = "Parameter is ready only";
                    break;
                case 7:
                    serverErrorMessage = "Parameter Value is out of range";
                    break;
                case 8:
                    serverErrorMessage = "Parameter Instance is not available";
                    break;
                case 9:
                    serverErrorMessage = "Parameter general failure.";
                    break;
                default:
                    serverErrorMessage = "Unknown Server Error Code: " + ErrorCode;
                    break;
            }
            throw new ServerException(serverErrorMessage, ErrorCode);
        }

        void CheckIfConnectedOrException()
        {
            //If the interface is not ready and the current thread is not the creator of this instance, throw exception
            if (!isReady && Thread.CurrentThread.ManagedThreadId != threadIdOfCreator)
                throw new NotConnectedException();
        }

        /// <summary>
        /// Is used when the server has returned a Server Error Code.
        /// </summary>
        public class ServerException : Exception
        {
            /// <summary>
            /// Stores the Server Error Code.
            /// </summary>
            public int ServerErrorCode { get; set; }

            /// <summary>
            /// Initializes a new instance of ServerException with the given parameters.
            /// </summary>
            /// <param name="message">Server Error Message.</param>
            /// <param name="ErrorCode">Server Error Code.</param>
            public ServerException(string message, int ErrorCode)
                : base(message)
            {
                ServerErrorCode = ErrorCode;
            }
        }

        /// <summary>
        /// Is used when the interface is not connected and a different thread than 
        /// the creator of this object tries to send data.
        /// </summary>
        public class NotConnectedException : Exception
        {
            /// <summary>
            /// Initializes a new instance of NotConnectedException.
            /// </summary>
            public NotConnectedException()
                : base("Interface is not Connected")
            {
            }
        }

        /// <summary>
        /// Is used to encapsulate all not specific exceptions.
        /// Check the inner exception for details.
        /// </summary>
        public class GeneralException : Exception
        {
            /// <summary>
            /// Initializes a new instance of ServerException with the given parameters.
            /// </summary>
            /// <param name="message">Error Message</param>
            public GeneralException(string message)
                : base(message)
            {
            }

            /// <summary>
            /// Initializes a new instance of ServerException with the given parameters.
            /// </summary>
            /// <param name="message">Error Message</param>
            /// <param name="innerException">Detail exception.</param>
            public GeneralException(string message, Exception innerException)
                : base(message, innerException)
            {
            }
        }
    }
}
