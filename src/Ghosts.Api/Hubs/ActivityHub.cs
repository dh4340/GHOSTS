// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Globalization;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;
using NLog;

namespace ghosts.api.Hubs;

public class ActivityHub : Hub
{
    internal static Logger _log = LogManager.GetCurrentClassLogger();

    private static readonly ConnectionMapping<string> _connections = new();

    public ActivityHub() { }

    public override Task OnConnectedAsync()
    {
        _connections.Add("1", Context.ConnectionId);
        return base.OnConnectedAsync();
    }

    public override Task OnDisconnectedAsync(Exception exception)
    {
        _connections.Remove("1", Context.ConnectionId);
        return base.OnDisconnectedAsync(exception);
    }

    public async Task Show(int eventId, string npcId, string type, string message, string time)
    {
        _log.Debug("Processing update");

        //do some saving

        foreach (var connectionId in _connections.GetConnections("1"))
        {
            var types = new[] { "social", "belief", "knowledge", "relationship" };
            var t = types.RandomFromStringArray();

            await Clients.Client(connectionId).SendAsync("show", eventId,
                npcId,
                t,
                Faker.Lorem.Sentence(),
                DateTime.Now.ToString(CultureInfo.InvariantCulture));
        }
    }
}
