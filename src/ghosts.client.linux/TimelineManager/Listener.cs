﻿// Copyright 2017 Carnegie Mellon University. All Rights Reserved. See LICENSE.md file for terms.

using System;
using System.IO;
using System.Linq;
using System.Threading;
using Ghosts.Domain;
using Ghosts.Domain.Code;
using Newtonsoft.Json;
using NLog;
using SimpleTCP;
// ReSharper disable ObjectCreationAsStatement

namespace ghosts.client.linux.timelineManager
{
    public static class ListenerManager
    {
        private static readonly Logger _log = LogManager.GetCurrentClassLogger();
        private static readonly string In = ApplicationDetails.InstanceDirectories.TimelineIn;
        private static readonly string Out = ApplicationDetails.InstanceDirectories.TimelineOut;

        public static void Run()
        {
            try
            {
                if (Program.Configuration.Listener.Port > 0)
                {
                    var t = new Thread(() => { new Listener(); })
                    {
                        IsBackground = true,
                        Name = "ghosts-portlistener"
                    };
                    t.Start();
                }
            }
            catch (Exception e)
            {
                _log.Debug(e);
            }

            try
            {
                if (!string.IsNullOrEmpty(In) && !string.IsNullOrEmpty(Out))
                {
                    if (!Directory.Exists(In))
                    {
                        Directory.CreateDirectory(In);
                        _log.Trace($"DirectoryListener created DirIn: {In})");
                    }

                    if (!Directory.Exists(Out))
                    {
                        Directory.CreateDirectory(Out);
                        _log.Trace($"DirectoryListener created DirIn: {Out})");
                    }

                    var t = new Thread(() => { new DirectoryListener(); })
                    {
                        IsBackground = true,
                        Name = "ghosts-directorylistener"
                    };
                    t.Start();
                    
                    t = new Thread(() => { new InitialDirectoryListener(); })
                    {
                        IsBackground = true,
                        Name = "ghosts-initialdirectorylistener"
                    };
                    t.Start();
                    
                    EnsureWatch();
                }
                else
                {
                    _log.Trace("DirectoryListener is not configured (DirIn or DirOut is blank)");
                }
            }
            catch (Exception e)
            {
                _log.Debug(e);
            }
        }

        private static void EnsureWatch()
        {
            File.WriteAllText(In + "init.json", JsonConvert.SerializeObject(new Timeline(), Formatting.None));
        }
    }

    public class InitialDirectoryListener
    {
        private static readonly Logger _log = LogManager.GetCurrentClassLogger();
        private static DateTime _lastRead = DateTime.Now;
        public InitialDirectoryListener()
        {
            var directoryName = TimelineBuilder.TimelineFilePath().DirectoryName;
            if (directoryName == null)
            {
                throw new Exception("Timeline builder path cannot be determined");
            }
            
            var timelineWatcher = new FileSystemWatcher(directoryName);
            timelineWatcher.Filter = Path.GetFileName(TimelineBuilder.TimelineFilePath().Name);
            _log.Trace($"watching {timelineWatcher.Path}");
            timelineWatcher.NotifyFilter = NotifyFilters.LastAccess | NotifyFilters.FileName | NotifyFilters.Size | NotifyFilters.CreationTime |
                                           NotifyFilters.LastWrite;
            timelineWatcher.Changed += InitialOnChanged;
            timelineWatcher.EnableRaisingEvents = true;
        

            new ManualResetEvent(false).WaitOne();
        }
        
        private static void InitialOnChanged(object source, FileSystemEventArgs e)
        {
            // file watcher throws two events, we only need 1
            var lastWriteTime = File.GetLastWriteTime(e.FullPath);
            if (lastWriteTime <= _lastRead.AddSeconds(1)) return;
            
            _lastRead = lastWriteTime;
            _log.Trace("File: " + e.FullPath + " " + e.ChangeType);
            
            var method = string.Empty;
            if (System.Reflection.MethodBase.GetCurrentMethod() != null)
            {
                var declaringType = System.Reflection.MethodBase.GetCurrentMethod()?.DeclaringType;
                if (declaringType != null)
                    method = declaringType.ToString();
            }
            _log.Trace($"Reloading {method}...");

            // now terminate existing tasks and rerun
            var o = new Orchestrator();
            Orchestrator.Stop();
            o.Run();
        }
    }
    
    /// <summary>
    /// Watches a directory [ghosts install] \ instance \ timeline for dropped files, and processes them immediately
    /// </summary>
    public class DirectoryListener
    {
        private static readonly Logger _log = LogManager.GetCurrentClassLogger();
        private readonly string _in = ApplicationDetails.InstanceDirectories.TimelineIn;
        private readonly string _out = ApplicationDetails.InstanceDirectories.TimelineOut;
        private string _currentlyProcessing = string.Empty;
        
        public DirectoryListener()
        {
            var watcher = new FileSystemWatcher
            {
                Path = _in,
                NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName,
                Filter = "*.*"
            };
            watcher.Changed += OnChanged;
            watcher.Created += OnChanged;
            watcher.EnableRaisingEvents = true;
            new ManualResetEvent(false).WaitOne();
        } 
        
        private void OnChanged(object source, FileSystemEventArgs e)
        {
            // file watcher throws multiple events, we only need 1
            if (!string.IsNullOrEmpty(_currentlyProcessing) && _currentlyProcessing == e.FullPath) return;
            _currentlyProcessing = e.FullPath;

            _log.Trace("DirectoryListener found file: " + e.FullPath + " " + e.ChangeType);

            if (!File.Exists(e.FullPath))
                return;

            if (e.FullPath.EndsWith(".json"))
            {
                try
                {
                    var timeline = TimelineBuilder.GetLocalTimeline(e.FullPath);
                    foreach (var timelineHandler in timeline.TimeLineHandlers)
                    {
                        _log.Trace($"DirectoryListener command found: {timelineHandler.HandlerType}");

                        foreach (var timelineEvent in timelineHandler.TimeLineEvents.Where(timelineEvent => string.IsNullOrEmpty(timelineEvent.TrackableId)))
                        {
                            timelineEvent.TrackableId = Guid.NewGuid().ToString();
                        }

                        Orchestrator.RunCommand(timeline, timelineHandler);
                    }
                }
                catch (Exception exc)
                {
                    _log.Debug(exc);
                }
            }
            else if (e.FullPath.EndsWith(".cs"))
            {
                try
                {
                    var commands = File.ReadAllText(e.FullPath).Split(Convert.ToChar("\n")).ToList();
                    if (commands.Count > 0)
                    {
                        var constructedTimelineHandler = TimelineTranslator.FromBrowserUnitTests(commands);
                        
                        var t = new Timeline
                        {
                            Id = Guid.NewGuid(),
                            Status = Timeline.TimelineStatus.Run
                        };
                        t.TimeLineHandlers.Add(constructedTimelineHandler);
                        Orchestrator.RunCommand(t, constructedTimelineHandler);
                    }
                }
                catch (Exception exc)
                {
                    _log.Debug(exc);
                }
            }

            try
            {
                var outfile = e.FullPath.Replace(_in, _out);
                outfile = outfile.Replace(e.Name, $"{DateTime.Now.ToString("G").Replace("/", "-").Replace(" ", "").Replace(":", "")}-{e.Name}");

                File.Move(e.FullPath, outfile);
            }
            catch (Exception exception)
            {
                _log.Debug(exception);
            }

            _currentlyProcessing = string.Empty;
        }
    }

    public class Listener
    {
        private static readonly Logger _log = LogManager.GetCurrentClassLogger();

        public Listener()
        {
            try
            {
                var server = new SimpleTcpServer().Start(Program.Configuration.Listener.Port);
                server.AutoTrimStrings = true;
                server.Delimiter = 0x13;

                Console.WriteLine($"Listener active on {string.Join(",", server.GetListeningIPs())} : {Program.Configuration.Listener.Port}");

                server.DataReceived += (sender, message) =>
                {
                    var obj = Handle(message);
                    message.ReplyLine($"{obj}{Environment.NewLine}");
                    Console.WriteLine(obj);
                };
            }
            catch (Exception e)
            {
                _log.Trace(e);
            }
        }

        private static string Handle(Message message)
        {
            var command = message.MessageString;
            var index = command.LastIndexOf("}", StringComparison.InvariantCultureIgnoreCase);
            if (index > 0)
                command = command[..(index + 1)];

            _log.Trace($"Received from {message.TcpClient.Client.RemoteEndPoint}: {command}");

            try
            {
                var timelineHandler = JsonConvert.DeserializeObject<TimelineHandler>(command);

                foreach (var evs in timelineHandler.TimeLineEvents.Where(evs => string.IsNullOrEmpty(evs.TrackableId)))
                {
                    evs.TrackableId = Guid.NewGuid().ToString();
                }

                _log.Trace($"Command found: {timelineHandler.HandlerType}");

                var t = new Timeline
                {
                    Id = Guid.NewGuid(),
                    Status = Timeline.TimelineStatus.Run
                };
                t.TimeLineHandlers.Add(timelineHandler);
                
                Orchestrator.RunCommand(t, timelineHandler);

                var obj = JsonConvert.SerializeObject(timelineHandler);

                return obj;
            }
            catch (Exception e)
            {
                _log.Trace(e);
            }

            return null;
        }
    }
}