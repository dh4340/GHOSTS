// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Linq;
using ghosts.client.linux.Infrastructure;
using ghosts.client.linux.timelineManager;
using Ghosts.Domain.Code;
using Ghosts.Domain.Messages;

namespace ghosts.client.linux.handlers
{
    public class NpcSystem : BaseHandler
    {
        public NpcSystem(Timeline timeline, TimelineHandler handler)
        {
            _log.Trace($"Handling NpcSystem call: {handler}");

            foreach (var timelineEvent in handler.TimeLineEvents.Where(timelineEvent => !string.IsNullOrEmpty(timelineEvent.Command)))
            {
                Timeline t;

                switch (timelineEvent.Command.ToLower())
                {
                    case "start":
                        t = TimelineBuilder.GetTimeline();
                        t.Status = Timeline.TimelineStatus.Run;
                        TimelineBuilder.SetLocalTimeline(t);
                        break;
                    case "stop":
                        if (timeline.Id != Guid.Empty)
                        {
                            Orchestrator.StopTimeline(timeline.Id);
                        }
                        else
                        {
                            t = TimelineBuilder.GetTimeline();
                            t.Status = Timeline.TimelineStatus.Stop;
                            StartupTasks.CleanupProcesses();
                            TimelineBuilder.SetLocalTimeline(t);
                        }

                        break;
                }
            }
        }
    }
}
