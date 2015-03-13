using System;
using DefaultCommands.Commands;
using Spiff.Core.API;

namespace DefaultCommands
{
    public class DefaultCommands : Plugin
    {
        public override string Name
        {
            get { return "Default Commands"; }
        }

        public override string Author
        {
            get { return "Toyz"; }
        }

        public override string Description
        {
            get { return "This is default  commands that ship with this bot"; }
        }

        public override void Start()
        {
            Console.WriteLine("[Default Commands]Loading Plugin Commands");
            RegisterCommand(new AllCommands());
            RegisterCommand(new HelpCommand());
            RegisterCommand(new GameCommand());
            RegisterCommand(new RandomViewer());
        }

        public override void Destory()
        {
            Console.WriteLine("[Default Commands]Stopping");
        }
    }
}
