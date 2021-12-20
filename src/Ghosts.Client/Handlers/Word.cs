// Copyright 2017 Carnegie Mellon University. All Rights Reserved. See LICENSE.md file for terms.

using Ghosts.Client.Infrastructure;
using Ghosts.Domain;
using Ghosts.Domain.Code;
using NetOffice.WordApi.Enums;
using NLog;
using System;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Threading;
using Ghosts.Domain.Code.Helpers;
using Word = NetOffice.WordApi;
using VB = Microsoft.VisualBasic;

namespace Ghosts.Client.Handlers
{
    public class WordHandler : BaseHandler
    {
        private static readonly Logger _log = LogManager.GetCurrentClassLogger();

        public WordHandler(Timeline timeline, TimelineHandler handler)
        {
            _log.Trace("Launching Word handler");
            try
            {
                if (handler.Loop)
                {
                    _log.Trace("Word loop");
                    while (true)
                    {
                        if (timeline != null)
                        {
                            System.Collections.Generic.List<int> processIds = ProcessManager.GetPids(ProcessManager.ProcessNames.Word).ToList();
                            if (processIds.Count > timeline.TimeLineHandlers.Count(o => o.HandlerType == HandlerType.Word))
                            {
                                continue;
                            }
                        }

                        ExecuteEvents(timeline, handler);
                    }
                }
                else
                {
                    _log.Trace("Word single run");
                    KillApp();
                    ExecuteEvents(timeline, handler);
                    KillApp();
                }
            }
            catch (Exception e)
            {
                _log.Error(e);
                KillApp();
            }
        }

        private static void KillApp()
        {
            ProcessManager.KillProcessAndChildrenByName(ProcessManager.ProcessNames.Word);
        }

        private void ExecuteEvents(Timeline timeline, TimelineHandler handler)
        {
            try
            {
                foreach (var timelineEvent in handler.TimeLineEvents)
                {
                    try
                    {
                        _log.Trace($"Word event - {timelineEvent}");
                        WorkingHours.Is(handler);

                        if (timelineEvent.DelayBefore > 0)
                        {
                            Thread.Sleep(timelineEvent.DelayBefore);
                        }

                        if (timeline != null)
                        {
                            var processIds = ProcessManager.GetPids(ProcessManager.ProcessNames.Word).ToList();
                            if (processIds.Count > timeline.TimeLineHandlers.Count(o => o.HandlerType == HandlerType.Word))
                            {
                                return;
                            }
                        }

                        // start word and turn off msg boxes
                        var wordApplication = new Word.Application
                        {
                            DisplayAlerts = WdAlertLevel.wdAlertsNone,
                            Visible = true
                        };

                        // add a new document
                        var newDocument = wordApplication.Documents.Add();

                        try
                        {
                            wordApplication.WindowState = WdWindowState.wdWindowStateMinimize;
                            foreach (var item in wordApplication.Documents)
                            {
                                item.Windows[1].WindowState = WdWindowState.wdWindowStateMinimize;
                            }
                        }
                        catch (Exception e)
                        {
                            _log.Trace($"Could not minimize: {e}");
                        }
                        
                        // insert some text
                        var list = RandomText.GetDictionary.GetDictionaryList();
                        var rt = new RandomText(list.ToArray());
                        rt.AddContentParagraphs(1, 50);
                        wordApplication.Selection.TypeText(rt.Content);

                        var writeSleep = ProcessManager.Jitter(100);
                        Thread.Sleep(writeSleep);

                        wordApplication.Selection.HomeKey(WdUnits.wdLine, WdMovementType.wdExtend);
                        wordApplication.Selection.Font.Color = GetWdColor(StylingExtensions.GetRandomColor());
                        wordApplication.Selection.Font.Bold = 1;
                        wordApplication.Selection.Font.Size = 12;

                        var rand = RandomFilename.Generate();

                        var dir = timelineEvent.CommandArgs[0].ToString();
                        if (dir.Contains("%"))
                        {
                            dir = Environment.ExpandEnvironmentVariables(dir);
                        }

                        if (Directory.Exists(dir))
                        {
                            Directory.CreateDirectory(dir);
                        }

                        var path = $"{dir}\\{rand}.docx";

                        //if directory does not exist, create!
                        _log.Trace($"Checking directory at {path}");
                        var f = new FileInfo(path).Directory;
                        if (f == null)
                        {
                            _log.Trace($"Directory does not exist, creating directory at {f.FullName}");
                            Directory.CreateDirectory(f.FullName);
                        }

                        try
                        {
                            if (File.Exists(path))
                            {
                                File.Delete(path);
                            }
                        }
                        catch (Exception e)
                        {
                            _log.Debug(e);
                        }

                        newDocument.Saved = true;
                        newDocument.SaveAs(path);

                        Report(handler.HandlerType.ToString(), timelineEvent.Command, timelineEvent.CommandArgs[0].ToString());
                        FileListing.Add(path);

                        if (timelineEvent.CommandArgs.Contains("pdf"))
                        {
                            // Save document into PDF Format
                            object oMissing = System.Reflection.Missing.Value;
                            object outputFileName = timelineEvent.CommandArgs.Contains("pdf-vary-filenames") ? $"{RandomFilename.Generate()}.pdf" : newDocument.FullName.Replace(".docx", ".pdf");
                            object fileFormat = WdSaveFormat.wdFormatPDF;

                            newDocument.SaveAs(outputFileName, fileFormat, oMissing, oMissing,
                                oMissing, oMissing, oMissing, oMissing,
                                oMissing, oMissing, oMissing, oMissing,
                                oMissing, oMissing, oMissing, oMissing);
                            // end save as pdf
                            Report(handler.HandlerType.ToString(), timelineEvent.Command, "pdf");
                            FileListing.Add(outputFileName.ToString());
                        }

                        newDocument.Close();

                        if (timelineEvent.DelayAfter > 0)
                        {
                            //sleep and leave the app open
                            _log.Trace($"Sleep after for {timelineEvent.DelayAfter}");
                            Thread.Sleep(timelineEvent.DelayAfter - writeSleep);
                        }

                        wordApplication.Quit();
                        wordApplication.Dispose();
                        wordApplication = null;

                        try
                        {
                            Marshal.ReleaseComObject(wordApplication);
                        }
                        catch
                        {
                            // ignore
                        }

                        try
                        {
                            Marshal.FinalReleaseComObject(wordApplication);
                        }
                        catch
                        {
                            // ignore
                        }

                        GC.Collect();
                    }
                    catch (Exception e)
                    {
                        _log.Debug(e);
                    }
                    finally
                    {
                        Thread.Sleep(5000);
                    }
                }
            }
            catch (Exception e)
            {
                _log.Error(e);
            }
            finally
            {
                KillApp();
                _log.Trace("Word closing...");
            }
        }


        private WdColor GetWdColor(Color color)
        {
            var rgbColor = VB.Information.RGB(color.R, color.G, color.B);
            var wdColor = (WdColor)rgbColor;
            return wdColor;
        }
    }
}