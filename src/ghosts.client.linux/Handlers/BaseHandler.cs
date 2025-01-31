// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using Ghosts.Domain.Code;
using Ghosts.Domain.Messages;

namespace ghosts.client.linux.handlers
{
    public abstract class BaseHandler
    {
        public static readonly Logger _log = LogManager.GetCurrentClassLogger();
        private static readonly Logger _timelineLog = LogManager.GetLogger("TIMELINE");
        internal static readonly Random _random = new();

        public static void Init(TimelineHandler handler)
        {
            WorkingHours.Is(handler);
        }

        public static void Report(ReportItem reportItem)
        {
            var result = new TimeLineRecord
            {
                Handler = reportItem.Handler,
                Command = reportItem.Command,
                CommandArg = reportItem.Arg,
                Result = reportItem.Result,
                TrackableId = reportItem.Trackable
            };

            var o = JsonConvert.SerializeObject(result,
                Formatting.None,
                new JsonSerializerSettings
                {
                    NullValueHandling = NullValueHandling.Ignore
                });

            _timelineLog.Info($"TIMELINE|{DateTime.UtcNow}|{o}");
        }
    }

}
