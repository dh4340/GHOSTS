// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections.Generic;
using NLog;

namespace ghosts.api.Infrastructure.Extensions;

public static class EnumeratorExtensions
{
    private static readonly Logger _log = LogManager.GetCurrentClassLogger();

    public static string GetRandom(this IList<string> list, Random random)
    {
        try
        {
            return list.Count < 1 ? "" : list[random.Next(list.Count)];
        }
        catch (Exception e)
        {
            _log.Error(e);
            return "";
        }
    }
}
