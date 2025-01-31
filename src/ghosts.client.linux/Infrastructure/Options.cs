// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

namespace ghosts.client.linux.Infrastructure
{
    /// <summary>
    /// Defines the flags you can send to the client
    /// </summary>
    internal class Options
    {
        [Option('d', "debug", Default = false, HelpText = "Launch GHOSTS in debug mode")]
        public bool Debug { get; set; }

        [Option('h', "help", Default = false, HelpText = "Display this help screen")]
        public bool Help { get; set; }

        [Option('r', "randomize", Default = false, HelpText = "Create a randomized timeline")]
        public bool Randomize { get; set; }

        [Option('v', "version", Default = false, HelpText = "GHOSTS client version")]
        public bool Version { get; set; }

        [Option('i', "information", Default = false, HelpText = "GHOSTS client id information")]
        public bool Information { get; set; }
    }
}
