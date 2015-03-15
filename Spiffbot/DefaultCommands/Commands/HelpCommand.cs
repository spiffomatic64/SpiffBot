using Spiff.Core;
using Spiff.Core.API.Commands;

namespace DefaultCommands.Commands
{
    public class HelpCommand : Command
    {
        public override string CommandName
        {
            get { return "help"; }
        }

        public override string CommandInfo
        {
            get { return "Get the help info for a given command name"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            if (parts.Length < 2)
            {
                Boardcast("Usage: !help commandname");
                return;
            }

            Command command;

            TwitchIRC.Instance.AllCommands().TryGetValue("!" + parts[1], out command);

            if (command == null)
                Boardcast("Command does not exist");
            else
                Boardcast(command.CommandName + " - " + command.CommandInfo);
        }
    }
}
