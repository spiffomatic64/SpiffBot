using Spiff.Core;
using Spiff.Core.API.Commands;

namespace CustomCommands.Commands
{
    public class SourceCommand : Command
    {
        public override string CommandName
        {
            get { return "source"; }
        }

        public override string CommandInfo
        {
            get { return "This is a link to the source code on github"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            TwitchIRC.Instance.WriteOut.SendMessage(string.Format("Hey, {0} here is a link to the code: https://github.com/Toyz/SpiffBot/tree/master/Spiffbot", nick), channel);
        }
    }
}
