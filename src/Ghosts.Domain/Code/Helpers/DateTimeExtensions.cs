// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.IO;

namespace Ghosts.Domain.Code.Helpers
{
    public static class DateTimeExtensions
    {
        public static bool IsOlderThanHours(string filename, int hours)
        {
            var threshold = DateTime.Now.AddHours(-hours);
            return File.GetCreationTime(filename) <= threshold;
        }
    }
}
