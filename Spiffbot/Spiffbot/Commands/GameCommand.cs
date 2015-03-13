using Spiff.Core;
using Spiff.Core.API.Commands;

namespace Spiffbot.Commands
{
    public class GameCommand : ICommand
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
            var game = TwitchAPI.GetGame(channel);

            TwitchIRC.Instance.WriteOut.SendMessage(channel + " is currently playing: " + (string.IsNullOrEmpty(game) ? "Nothing" : game), channel);
        }
    }
}
