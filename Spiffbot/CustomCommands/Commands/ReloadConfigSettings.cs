using Spiff.Core.API.Commands;

namespace CustomCommands.Commands
{
    public class ReloadConfigSettings : Command
    {
        public override string CommandName
        {
            get { return "songreload"; }
        }

        public override string CommandInfo
        {
            get { return "Reload the config for the song"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            if (IsOwner(nick))
            {
                CustomCommands.ConfigSettings.Refresh();
                Boardcast(nick + " has reloaded the config");
            }
        }
    }
}
