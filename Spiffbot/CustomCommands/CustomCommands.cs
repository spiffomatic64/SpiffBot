using CustomCommands.Commands;
using Spiff.Core.API;

namespace CustomCommands
{
    public class CustomCommands : Plugin
    {
        public override string Name
        {
            get { return "Custom Commands"; }
        }

        public override string Author
        {
            get { return "Toyz"; }
        }

        public override string Description
        {
            get { return "A few custom commands for my stream"; }
        }

        public override void Start()
        {
            RegisterCommand(new SourceCommand());
        }

        public override void Destory()
        {
            
        }
    }
}
