// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace ghosts.api.Infrastructure.Models
{
    [JsonConverter(typeof(StringEnumConverter))]
    public enum StatusType
    {
        Active = 0,
        Deleted = -9
    }
}
