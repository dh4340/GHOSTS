// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ghosts.api.Infrastructure.Models
{
    [Table("machine_timelines")]
    public class MachineTimeline
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }

        [ForeignKey("MachineId")]
        public Guid MachineId { get; set; }

        /// <summary>
        /// This is a string unfortunately, because EF can't handle string arrays, etc.
        /// </summary>
        [Column(TypeName = "jsonb")]
        public string Timeline { get; set; }

        public DateTime CreatedUtc { get; set; }

        public MachineTimeline()
        {
            CreatedUtc = DateTime.UtcNow;
        }
    }
}
