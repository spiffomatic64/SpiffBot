using Spiff.Core;
using Spiff.Core.API.Commands;
using Spiff.Core.API.Twitch;
using Spiff.Core.Extensions;

namespace DefaultCommands.Commands
{
    public class RandomViewer : Command
    {
        public override string CommandName
        {
            get { return "rndviewer"; }
        }

        public override string CommandInfo
        {
            get { return "Return a random viewer fom the chat"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            var viewers = SiteApi.GetChatters(channel);

            Boardcast("Random User is: " + viewers.PickRandom().Username);
        }
    }
}
