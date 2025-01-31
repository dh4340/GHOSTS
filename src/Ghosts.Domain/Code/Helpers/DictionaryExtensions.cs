// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Collections.Generic;

namespace Ghosts.Domain.Code.Helpers
{
    public static class DictionaryExtensions
    {
        public static bool ContainsKeyWithOption(this Dictionary<string, object> options, string key, string value)
        {
            return options.ContainsKey(key) && (string)options[key] == value;
        }
    }
}
