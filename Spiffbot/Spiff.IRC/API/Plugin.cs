using Spiff.Core.API.Commands;

namespace Spiff.Core.API
{
    public abstract class Plugin
    {
        //Plugin Info
        public abstract string Name { get; }
        public abstract string Author { get; }
        public abstract string Description { get; }

        public abstract void Start();

        public abstract void Destory();

        protected void RegisterCommand(ICommand command)
        {
            TwitchIRC.Instance.AddCommand(command);
        }
    }
}
