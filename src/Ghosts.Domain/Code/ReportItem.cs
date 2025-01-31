// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

namespace Ghosts.Domain.Code
{
    public class ReportItem
    {
        public string Handler { get; set; }
        public string Command { get; set; }
        public string Arg { get; set; }
        public string Trackable { get; set; }
        public string Result { get; set; }
    }
}
