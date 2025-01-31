// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ghosts.api.Infrastructure.Models
{
    [Table("trackables")]
    public class Trackable
    {
        [Key] public Guid Id { get; set; }

        [ForeignKey("MachineId")] public Guid MachineId { get; set; }

        public string Name { get; set; }
    }
}
