// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;

namespace ghosts.client.linux.Infrastructure;

public static class KnownFolders
{
    public static string GetHomePath()
    {
        return Environment.ExpandEnvironmentVariables("%HOME%");
    }

    public static string GetDownloadFolderPath()
    {
        return GetHomePath() + "/Downloads";
    }
}
