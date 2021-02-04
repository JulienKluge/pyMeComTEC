using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace MeSoft.MeCom.Core
{
    /// <summary>
    /// Is used when a communication command to the server fails.
    /// Check the inner exception for details.
    /// </summary>
    public class ComCommandException : Exception
    {
        /// <summary>
        /// Initializes a new instance of ComCommandException with the given parameters.
        /// </summary>
        /// <param name="message">Exception message.</param>
        public ComCommandException(string message)
            : base(message)
        {
        }

        /// <summary>
        /// Initializes a new instance of ComCommandException with the given parameters.
        /// Check the innerException for details.
        /// </summary>
        /// <param name="message">Exception message.</param>
        /// <param name="innerException">Inner Exception</param>
        public ComCommandException(string message, Exception innerException)
            : base(message, innerException)
        {
        }
    }
}
