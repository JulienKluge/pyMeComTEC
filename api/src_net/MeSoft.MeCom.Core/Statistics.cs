using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Threading;

namespace MeSoft.MeCom.Core
{
    /// <summary>
    /// Communication statistic class.
    /// Observes each call to the communication interface.
    /// Each calling thread is individually observed.
    /// Call every 10s GetStatistics to generate the current statistic data.
    /// </summary>
    public class Statistics
    {
        object lockObj = new object();
        Dictionary<int, StatData> statDataDict = new Dictionary<int, StatData>();
        Stopwatch totalTimeStopwatch;
        Stopwatch intervalStopwatch;

        /// <summary>
        /// Calculates and returns the statistic data. 
        /// It is recommended to call this function every 1s or 10s and put the received data into a DataSet Table.
        /// It is not mandatory to use this, but the statistic data will be collected anyway.
        /// </summary>
        /// <param name="xmlTable">XML structure that is compatible with System.Data.DataSet</param>
        /// <param name="additionalText">Some additional information. May be displayed under the table.</param>
        public void GetStatistics(out string xmlTable, out string additionalText)
        {
            try
            {
                StringBuilder sb1 = new StringBuilder();
                StringBuilder sb2 = new StringBuilder();

                sb1.AppendLine("<Table>");
                intervalStopwatch.Stop();
                lock (lockObj)
                {
                    foreach (KeyValuePair<int, StatData> item in statDataDict)
                    {
                        StatData v = item.Value;
                        sb1.AppendLine("<Element>");
                        sb1.AppendFormat("<Thread>{0}:{2}{1}</Thread>", item.Key, v.Name, Environment.NewLine);
                        sb1.AppendFormat("<Scope>Total{0}Actual</Scope>", Environment.NewLine);
                        sb1.AppendFormat("<TxBytes>{0}B{2}{1}B</TxBytes>{2}", CExp(v.TotalTxBytes), CExp(v.TotalTxBytes - v.OldTxBytes), Environment.NewLine);
                        sb1.AppendFormat("<RxBytes>{0}B{2}{1}B</RxBytes>{2}", CExp(v.TotalRxBytes), CExp(v.TotalRxBytes - v.OldRxBytes), Environment.NewLine);
                        sb1.AppendFormat("<TxSpeed>{0}B{2}{1}B/s</TxSpeed>{2}", CExp(v.TotalTxBytes / totalTimeStopwatch.Elapsed.TotalSeconds), CExp((v.TotalTxBytes - v.OldTxBytes) / intervalStopwatch.Elapsed.TotalSeconds), Environment.NewLine);
                        sb1.AppendFormat("<RxSpeed>{0}B/s{2}{1}B/s</RxSpeed>{2}", CExp(v.TotalRxBytes / totalTimeStopwatch.Elapsed.TotalSeconds), CExp((v.TotalRxBytes - v.OldRxBytes) / intervalStopwatch.Elapsed.TotalSeconds), Environment.NewLine);
                        sb1.AppendFormat("<ComTime>{0}s{2}{1}s</ComTime>{2}", CExp(v.ComTimeStw.Elapsed.TotalSeconds), CExp((v.ComTimeStw.Elapsed - v.OldComTime).TotalSeconds), Environment.NewLine);
                        sb1.AppendFormat("<WaitTime>{0}s{2}{1}s</WaitTime>{2}", CExp(v.WaitTimeStw.Elapsed.TotalSeconds), CExp((v.WaitTimeStw.Elapsed - v.OldWaitTime).TotalSeconds), Environment.NewLine);
                        sb1.AppendFormat("<ComUsage>{0:N1} &#37;{2}{1:N1} &#37;</ComUsage>{2}", 100.0 / totalTimeStopwatch.Elapsed.TotalSeconds * v.ComTimeStw.Elapsed.TotalSeconds, 100.0 / intervalStopwatch.Elapsed.TotalSeconds * (v.ComTimeStw.Elapsed - v.OldComTime).TotalSeconds, Environment.NewLine);
                        sb1.AppendFormat("<TxFrames>{0}{2}{1}</TxFrames>{2}", v.TotalTxFrames, v.TotalTxFrames - v.OldTxFrames, Environment.NewLine);
                        sb1.AppendFormat("<RxFrames>{0}{2}{1}</RxFrames>{2}", v.TotalRxFrames, v.TotalRxFrames - v.OldRxFrames, Environment.NewLine);
                        sb1.AppendFormat("<CrcErrors>{0}{2}{1}</CrcErrors>{2}", v.TotalCrcErrors, v.TotalCrcErrors - v.OldCrcErrors, Environment.NewLine);
                        sb1.AppendLine("</Element>");

                        v.SetOldValues();
                    }
                }
                sb1.AppendLine("</Table>");
                xmlTable = sb1.ToString();

                sb2.AppendFormat("Actual Measuring Interval: {0:N1} s{1}", intervalStopwatch.Elapsed.TotalSeconds, Environment.NewLine);
                sb2.AppendFormat("Total Measuring Time: {0:N0} s{1}", totalTimeStopwatch.Elapsed.TotalSeconds, Environment.NewLine);
                additionalText = sb2.ToString();

                intervalStopwatch.Restart();
            }
            catch (Exception ex)
            {
                xmlTable = "";
                additionalText = ex.Message;
            }
        }

        /// <summary>
        /// Internal constructor. 
        /// Means this object can not be instantiated outside of this assembly. (Just because it is not necessary)
        /// </summary>
        internal Statistics()
        {
            try
            {
                totalTimeStopwatch = new Stopwatch();
                totalTimeStopwatch.Start();
                intervalStopwatch = new Stopwatch();
                intervalStopwatch.Start();
            }
            catch { }
        }


        internal void ThreadWaitForLock()
        {
            try
            {
                lock (lockObj)
                {
                    StatData stat = CheckIfThredIdIsPresentOrCreate(Thread.CurrentThread.ManagedThreadId);
                    stat.WaitTimeStw.Start();
                }
            }
            catch { }
  
        }
        internal void ThreadLockEntered()
        {
            try
            {
                lock (lockObj)
                {
                    StatData stat = statDataDict[Thread.CurrentThread.ManagedThreadId];
                    stat.WaitTimeStw.Stop();
                    stat.ComTimeStw.Start();
                }
            }
            catch { }
        }
        internal void ThreadExited()
        {
            try
            {
                lock (lockObj)
                {
                    StatData stat = statDataDict[Thread.CurrentThread.ManagedThreadId];
                    stat.WaitTimeStw.Stop();
                    stat.ComTimeStw.Stop();
                }
            }
            catch { }
        }
        internal void AddTxBytes(long plus)
        {
            try
            {
                lock (lockObj) statDataDict[Thread.CurrentThread.ManagedThreadId].TotalTxBytes += plus;
            }
            catch { }    
        }
        internal void AddRxBytes(long plus)
        {
            try
            {
                lock (lockObj) statDataDict[Thread.CurrentThread.ManagedThreadId].TotalRxBytes += plus;
            }
            catch { }       
        }
        internal void IncTxFrames()
        {
            try
            {
                lock (lockObj) statDataDict[Thread.CurrentThread.ManagedThreadId].TotalTxFrames++;
            }
            catch { }
        }
        internal void IncRxFrames()
        {
            try
            {
                lock (lockObj) statDataDict[Thread.CurrentThread.ManagedThreadId].TotalRxFrames++;
            }
            catch { }
        }
        internal void IncCrcErrors()
        {
            try
            {
                lock (lockObj) statDataDict[Thread.CurrentThread.ManagedThreadId].TotalCrcErrors++;
            }
            catch { }     
        }


        StatData CheckIfThredIdIsPresentOrCreate(int id)
        {
            StatData stat;
            if (!statDataDict.TryGetValue(Thread.CurrentThread.ManagedThreadId, out stat))
            {
                stat = new StatData();
                stat.Name = Thread.CurrentThread.Name;
                statDataDict.Add(Thread.CurrentThread.ManagedThreadId, stat);
            }
            return stat;
        }

        string CExp(double value)
        {
            string[] units = {"p", "n", "u", "m", "", "K", "M", "G", "T", "P", "E", "Z", "Y"};
            int unit = 0;
            if (value != 0)
            {
                while (value >= 1000)
                {
                    value /= 1000;
                    unit++;
                }
                while (value < 1)
                {
                    value *= 1000;
                    unit--;
                }
            }
            return String.Format("{0:G4} {1}", value, units[unit+4]);
        }
        

        class StatData
        {
            internal string Name;
            internal long TotalTxBytes, OldTxBytes;
            internal long TotalRxBytes, OldRxBytes;

            internal long TotalTxFrames, OldTxFrames;
            internal long TotalRxFrames, OldRxFrames;
            internal long TotalCrcErrors, OldCrcErrors;


            internal Stopwatch WaitTimeStw = new Stopwatch();
            internal Stopwatch ComTimeStw = new Stopwatch();
            internal TimeSpan OldWaitTime;
            internal TimeSpan OldComTime;

            internal void SetOldValues()
            {
                OldTxBytes = TotalTxBytes;
                OldRxBytes = TotalRxBytes;
                OldTxFrames = TotalTxFrames;
                OldRxFrames = TotalRxFrames;
                OldCrcErrors = TotalCrcErrors;
                OldWaitTime = WaitTimeStw.Elapsed;
                OldComTime = ComTimeStw.Elapsed;
            }
        }
    }
}
