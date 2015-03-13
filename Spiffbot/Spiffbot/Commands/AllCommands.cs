using Spiff.IRC;
using Spiff.IRC.API.Commands;

namespace Spiffbot.Commands
{
    public class AllCommands : ICommand
    {
        public override string CommandName
        {
            get { return "allcmd"; }
        }

        public override string CommandInfo
        {
            get { return "Returns a list of all possible commands"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            var commands = string.Join(", ", TwitchIRC.Instance.AllCommands().Keys);

            TwitchIRC.Instance.WriteOut.SendMessage("All Commands: " + commands, channel);
        }
    }
}
