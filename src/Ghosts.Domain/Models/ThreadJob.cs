// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Threading;

namespace Ghosts.Domain.Models
{
    public class ThreadJob
    {
        public Guid TimelineId { get; set; }
        public Thread Thread { get; set; }
    }
}
