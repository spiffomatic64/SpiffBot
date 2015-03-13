using Spiff.Core;
using Spiff.Core.API.Commands;

namespace DefaultCommands.Commands
{
    public class HelpCommand : ICommand
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
                TwitchIRC.Instance.WriteOut.SendMessage("Usage: !help commandname", channel);
                return;
            }

            ICommand command;

            TwitchIRC.Instance.AllCommands().TryGetValue("!" + parts[1], out command);

            if (command == null)
                TwitchIRC.Instance.WriteOut.SendMessage("Command does not exist", channel);
            else
                TwitchIRC.Instance.WriteOut.SendMessage(command.CommandName + " - " + command.CommandInfo, channel);
        }
    }
}
