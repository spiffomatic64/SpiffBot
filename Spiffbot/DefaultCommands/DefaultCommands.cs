using DefaultCommands.Commands;
using Spiff.Core.API;
using Spiff.Core.Utils;

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
            Logger.Write("Loading Plugin Commands", Name);
            RegisterCommand(new AllCommands());
            RegisterCommand(new HelpCommand());
            RegisterCommand(new GameCommand());
            RegisterCommand(new RandomViewer());
            RegisterCommand(new PluginsCommand());
        }

        public override void Destory()
        {
            Logger.Write("[Default Commands]Stopping", Name);
        }
    }
}
