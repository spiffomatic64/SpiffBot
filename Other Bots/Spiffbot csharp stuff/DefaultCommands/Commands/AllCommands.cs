using Spiff.Core;
using Spiff.Core.API.Commands;

namespace DefaultCommands.Commands
{
    public class AllCommands : Command
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
            var commands = string.Join(", ", SpiffCore.Instance.AllCommands().Keys);

            Boardcast("All Commands: " + commands);
        }
    }
}
