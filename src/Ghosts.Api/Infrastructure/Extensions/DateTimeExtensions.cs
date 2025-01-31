// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;

namespace ghosts.api.Infrastructure.Extensions;

public static class DateTimeExtensions
{
    public static DateTime ToDateTime(this long unixMilliseconds)
    {
        var epochStart = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        var postCreationDate = epochStart.AddMilliseconds(unixMilliseconds);
        return postCreationDate;
    }
}
