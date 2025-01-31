// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Collections.Generic;

namespace Ghosts.Domain.Messages.MesssagesForServer
{
    /// <summary>
    ///     the client results of running a health check
    /// </summary>
    public class ResultHealth
    {
        public ResultHealth()
        {
            Errors = new List<string>();
            LoggedOnUsers = new List<string>();
            Stats = new MachineStats();
        }

        public bool Internet { get; set; }
        public bool Permissions { get; set; }
        public long ExecutionTime { get; set; }

        public List<string> Errors { get; set; }
        public List<string> LoggedOnUsers { get; set; }
        public MachineStats Stats { get; set; }

        public class MachineStats
        {
            public float Memory { get; set; }
            public float Cpu { get; set; }
            public float DiskSpace { get; set; }
        }
    }
}
