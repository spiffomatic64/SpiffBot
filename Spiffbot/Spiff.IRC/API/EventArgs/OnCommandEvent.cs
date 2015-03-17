using Spiff.Core.API.Commands;

namespace Spiff.Core.API.EventArgs
{
    public class OnCommandEvent : System.EventArgs
    {
        public Command Command { get; private set; }
        public string[] Args { get; private set; }
        public string Complete { get; private set; }

        public OnCommandEvent(Command command, string[] args, string complete)
        {
            Command = command;
            Args = args;
            Complete = complete;
        }

    }
}
