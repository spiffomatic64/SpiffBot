using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using Newtonsoft.Json.Linq;
using Spiff.Core.Utils;

namespace Spiff.Core
{
    public static class TwitchAPI
    {
        public class Viewer
        {
            public bool IsMod { get; private set; }
            public string Username { get; private set; }

            public Viewer(string username, bool isMod)
            {
                IsMod = isMod;
                Username = username;
            }
        }

        public static string GetGame(string streamer)
        {
            using (var client = new WebClient())
            {
                var json = JObject.Parse(client.DownloadString(string.Format("https://api.twitch.tv/kraken/streams/{0}", streamer)));

                //Console.WriteLine(json["stream"]);
                try
                {
                    return (string) json["stream"]["game"];
                }
                catch (Exception e)
                {
                    return string.Empty;
                }
            }
        }

        public static List<Viewer> GetChatters(string streamer)
        {
            var users = new List<Viewer>();
            //https://tmi.twitch.tv/group/user/%s/chatters
            using (var client = new WebClient())
            {
                try
                {
                    var json =
                        JObject.Parse(
                            client.DownloadString(string.Format("https://tmi.twitch.tv/group/user/{0}/chatters",
                                streamer)));

                    users.AddRange(json["chatters"]["viewers"].Select(viewer => new Viewer((string) viewer, false)));
                    users.AddRange(json["chatters"]["moderators"].Select(viewer => new Viewer((string) viewer, true)));
                }
                catch (Exception e)
                {
                    //Logger.Error(e, "TwitchAPI");
                }
            }

            return users;
        } 
    }
}
