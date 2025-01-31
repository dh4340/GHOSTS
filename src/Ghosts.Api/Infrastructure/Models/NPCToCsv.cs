// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using FileHelpers;

namespace ghosts.api.Infrastructure.Models;

[DelimitedRecord(",")]
public class NPCToCsv
{
    public Guid Id { get; set; }
    public string Email { get; set; }
}
