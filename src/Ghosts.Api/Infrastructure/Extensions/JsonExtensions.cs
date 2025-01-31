// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Newtonsoft.Json;

namespace Ghosts.Api.Infrastructure.Extensions;

public static class JsonExtensions
{
    public static bool ContainsInvalidUnicode<T>(this T o)
    {
        var jsonString = JsonConvert.SerializeObject(o);
        return jsonString.Contains("\\u0000");
    }
}
