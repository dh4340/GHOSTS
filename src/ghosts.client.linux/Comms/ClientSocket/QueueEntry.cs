// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

namespace ghosts.client.linux.Comms.ClientSocket;

public class QueueEntry
{
    public enum Types
    {
        Id,
        Heartbeat,
        Message,
        MessageSpecific,
        Timeline
    }

    public object Payload { get; set; }
    public Types Type { get; set; }
}
