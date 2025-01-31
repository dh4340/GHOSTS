// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

// ReSharper disable UnusedMember.Global

namespace ghosts.client.linux.Infrastructure.Browser
{
    public class ExtendedConfiguration
    {
        public int Stickiness { get; set; }
        public int DepthMin { get; set; }
        public int DepthMax { get; set; }
        public object[] Sites { get; set; }

        public override string ToString()
        {
            return JsonConvert.SerializeObject(this);
        }

        public static ExtendedConfiguration Load(object o)
        {
            var commandArg = o.ToString();
            var result = new ExtendedConfiguration();
            if (commandArg == null || !commandArg.StartsWith("{")) return result;
            result = JsonConvert.DeserializeObject<ExtendedConfiguration>(commandArg);
            return result;
        }
    }
}
