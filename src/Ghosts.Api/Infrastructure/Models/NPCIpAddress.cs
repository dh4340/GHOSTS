// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ghosts.api.Infrastructure.Models;

[Table("ips")]
public class NPCIpAddress
{
    [Key]
    public int Id { get; set; }
    public Guid NpcId { get; set; }
    public string IpAddress { get; set; }
    public DateTime CreatedUTC { get; set; }

    public string Enclave { get; set; }

    public NPCIpAddress()
    {
        CreatedUTC = DateTime.UtcNow;
    }
}
