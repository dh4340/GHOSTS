// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Diagnostics;

namespace Ghosts.Domain.Code.Helpers
{
    public static class ProcessExtensions
    {
        public static void SafeKill(this Process process)
        {
            try
            {
                var info = new ProcessStartInfo
                {
                    RedirectStandardOutput = true,
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    FileName = "taskkill",
                    Arguments = $"/pid {process.Id} /F /T"
                };
                Process.Start(info);

            }
            catch
            {
                try
                {
                    process.Kill();
                }
                catch
                {
                    // ignore
                }
            }
            finally
            {
                try
                {
                    process.Dispose();
                    process = null;
                }
                catch
                {
                    // ignore
                }
            }
        }
    }
}
