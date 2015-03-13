using Spiff.Core;
using Spiff.Core.API.Commands;

namespace DefaultCommands.Commands
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
