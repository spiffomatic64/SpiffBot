using Spiff.Core.API.Commands;
using Win32API;

namespace CustomCommands.Commands
{
    public class MouseMouseCommand : Command
    {
        public override string CommandName
        {
            get { return "mousepos"; }
        }

        public override string CommandInfo
        {
            get { return "Set the mouse's current location on the screen"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            if (IsOwner(nick))
            {
                if (parts.Length < 3)
                    return;

                Mouse.Move(int.Parse(parts[1]), int.Parse(parts[2]));
                Boardcast(string.Format("Moved mouse to: {0}, {1}", parts[1], parts[2]));
            }
        }
    }
}
