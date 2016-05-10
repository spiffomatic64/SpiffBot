using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Spiff.Core.API.Twitch
{
    public class TwitchJson
    {
        //Add All json responses here
        public static class Followers
        {
            public class Links
            {
                public string self { get; set; }
            }

            public class Links2
            {
                public string self { get; set; }
            }

            public class User
            {
                public int _id { get; set; }
                public string name { get; set; }
                public string created_at { get; set; }
                public string updated_at { get; set; }
                public Links2 _links { get; set; }
                public string display_name { get; set; }
                public string logo { get; set; }
                public string bio { get; set; }
                public string type { get; set; }
            }

            public class Follow
            {
                public string created_at { get; set; }
                public Links _links { get; set; }
                public bool notifications { get; set; }
                public User user { get; set; }
            }

            public class Links3
            {
                public string self { get; set; }
                public string next { get; set; }
            }

            public class RootObject
            {
                public List<Follow> follows { get; set; }
                public int _total { get; set; }
                public Links3 _links { get; set; }
            }
        }
    }

    public static class SiteApi
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

        public static TwitchJson.Followers.RootObject GetFollowers(string streamer)
        {
            using (var client = new WebClient())
            {

                return
                    JsonConvert.DeserializeObject<TwitchJson.Followers.RootObject>(
                        client.DownloadString("https://api.twitch.tv/kraken/channels/" + streamer + "/follows"));
            }
        }
    }
}
