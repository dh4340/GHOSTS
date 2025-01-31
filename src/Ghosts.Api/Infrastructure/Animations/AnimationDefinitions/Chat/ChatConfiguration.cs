// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Collections.Generic;

namespace ghosts.api.Infrastructure.Animations.AnimationDefinitions.Chat;

public class ChatJobConfiguration
{
    public ChatPlatformConfiguration Chat { get; set; }
    public List<string> Replacements { get; set; }
    public List<string> Drops { get; set; }

    public List<string> Prompts { get; set; }

    public class ChatPlatformConfiguration
    {
        public string BaseUrl { get; set; }
        public string AdminUsername { get; set; }
        public string AdminPassword { get; set; }
        public string DefaultUserPassword { get; set; }
        public int AgentsPerBatch { get; set; }
    }
}
