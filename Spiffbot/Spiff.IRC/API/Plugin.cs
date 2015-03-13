using Spiff.Core.API.Commands;

namespace Spiff.Core.API
{
    public abstract class Plugin
    {
        public abstract TwitchIRC TwitchIrc { get; set; }

        public abstract void Start();

        public abstract void Destory();

        protected void RegisterCommand(ICommand command)
        {
            TwitchIRC.Instance.AddCommand(command);
        }
    }
}
