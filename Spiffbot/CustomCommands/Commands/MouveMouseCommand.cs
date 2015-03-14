using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Spiff.Core.API.Commands;

namespace CustomCommands.Commands
{
    public class MouveMouseCommand : Command
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
                Win32API.Mouse.Move(int.Parse(parts[1]), int.Parse(parts[2]));
            }
        }
    }
}
