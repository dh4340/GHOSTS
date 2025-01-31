// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Ghosts.Domain.Messages.MesssagesForClient;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using Newtonsoft.Json.Linq;

namespace ghosts.api.Infrastructure.Models
{
    public class QueueEntry
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public enum Types
        {
            Notification,
            Machine,
            Survey
        }

        public object Payload { get; set; }
        public Types Type { get; set; }
    }

    public class MachineQueueEntry
    {
        public Machine Machine { get; set; }
        public TransferLogDump LogDump { get; set; }
        public Machine.MachineHistoryItem.HistoryType HistoryType { get; set; }
    }

    public class NotificationQueueEntry
    {
        [JsonConverter(typeof(StringEnumConverter))]
        public enum NotificationType
        {
            Timeline = 0,
            WebhookCreate = 1,
            TimelineDelivered = 10
        }

        public NotificationType Type { get; set; }
        public JObject Payload { get; set; }
    }
}
