// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Threading.Tasks;
using ghosts.api.Infrastructure.Models;

namespace ghosts.api.Infrastructure.ContentServices;

public interface IFormatterService
{
    Task<string> GenerateNextAction(NpcRecord npc, string history);
    Task<string> GenerateTweet(NpcRecord npc);

    Task<string> ExecuteQuery(string prompt);
}
