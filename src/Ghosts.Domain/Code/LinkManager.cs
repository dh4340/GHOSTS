// Copyright 2017 Carnegie Mellon University. All Rights Reserved. See LICENSE.md file for terms.

using Ghosts.Domain.Code.Helpers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace Ghosts.Domain.Code
{
    public class Link
    {
        public Link()
        {
            Priority = 0;
        }

        public Uri Url { get; set; }
        /// <summary>
        /// Higher priority is more important
        /// </summary>
        public int Priority { get; set; }

        public bool WasBrowsed { get; set; }
    }

    public class LinkManager
    {
        public List<Link> Links { private set; get; }

        private readonly Uri _baseUri;
        private readonly Random _random = new Random();

        public LinkManager(Uri baseUri)
        {
            Links = new List<Link>();
            _baseUri = baseUri;
        }

        public void AddLink(string url, int priority)
        {
            if (!Uri.TryCreate(url, UriKind.RelativeOrAbsolute, out var uri))
            {
                return;
            }
            this.AddLink(uri, priority);
        }

        public void AddLink(Uri uri, int priority)
        {
            string[] validSchemes = {"http", "https"};
            if (!validSchemes.Contains(uri.Scheme))
            {
                return;
            }
            
            foreach (var link in Links)
            {
                if (Uri.Compare(uri, link.Url, UriComponents.Host | UriComponents.PathAndQuery, UriFormat.SafeUnescaped, StringComparison.OrdinalIgnoreCase) == 0)
                {
                    return;
                }
            }

            //truly a new link, add it
            try
            {
                Links.Add(new Link { Url = uri, Priority = priority });
            }
            catch (Exception e)
            {
                Console.WriteLine($"{uri} {e}");
            }
        }

        public Link Choose()
        {
            var pickList = new List<Link>();
            
            foreach (var link in Links)
            {
                try
                {
                    // give relative links priority
                    if ((link.Url.Scheme + link.Url.Host).Replace("www.", "").Equals((_baseUri.Scheme + _baseUri.Host).Replace("www.", ""), StringComparison.InvariantCultureIgnoreCase))
                    {
                        link.Priority += 1;
                    }
                    else if (link.Url.Scheme.Equals("file", StringComparison.InvariantCultureIgnoreCase))
                    {
                        link.Priority += 1;
                    }

                    pickList.Add(link);
                }
                catch (Exception e)
                {
                    Console.WriteLine($"{link.Url} : {e}");
                }
            }

            Links = pickList.OrderByDescending(o => o.Priority).ToList();

            if (Links.Count < 1)
            {
                return null;
            }

            var priority = Links.First().Priority;
            var chosen = Links.Where(x => x.Priority == priority).PickRandom();

            if (chosen.Url.Scheme.ToLower().StartsWith("file"))
            {
                try
                {
                    var bUrl = _baseUri.ToString();
                    if (bUrl.EndsWith("/"))
                    {
                        bUrl = bUrl.Substring(0, bUrl.Length - 1);
                    }

                    var thisUrl = chosen.Url.ToString().Replace("file://", "");

                    thisUrl = Regex.Replace(thisUrl, "////", "//");
                    if (thisUrl.StartsWith("/"))
                    {
                        thisUrl = thisUrl.Substring(1, thisUrl.Length - 1);
                    }

                    chosen.Url = new Uri($"{bUrl}/{thisUrl}");
                }
                catch (Exception e)
                {
                    Console.WriteLine($"{chosen.Url} : {e}");
                }
            }

            return chosen;
        }
    }
}