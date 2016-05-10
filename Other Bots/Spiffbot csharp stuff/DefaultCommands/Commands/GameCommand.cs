using Spiff.Core;
using Spiff.Core.API.Commands;
using Spiff.Core.API.Twitch;

namespace DefaultCommands.Commands
{
    public class GameCommand : Command
    {
        public override string CommandName
        {
            get { return "game"; }
        }

        public override string CommandInfo
        {
            get { return "Get's the current game I am playing"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            var game = SiteApi.GetGame(channel);

            Boardcast(channel + " is currently playing: " + (string.IsNullOrEmpty(game) ? "Nothing" : game));
        }
    }
}
