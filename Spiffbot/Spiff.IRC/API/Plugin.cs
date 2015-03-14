using System.IO;
using Spiff.Core.API.Commands;
using Spiff.Core.Utils;

namespace Spiff.Core.API
{
    public abstract class Plugin
    {
        //Plugin Info
        public abstract string Name { get; }
        public abstract string Author { get; }
        public abstract string Description { get; }

        private Ini _config;

        public Ini Config
        {
            get
            {
                if (_config == null)
                {
                    if (!Directory.Exists(Path.Combine("Plugins", Name)))
                    {
                        Directory.CreateDirectory(Path.Combine("Plugins", Name));
                    }
                    _config = new Ini(Path.Combine("Plugins", Name, "Config.ini"));
                }

                return _config;
            }
        }

        public abstract void Start();

        public abstract void Destory();

        protected void RegisterCommand(Command command)
        {
            TwitchIRC.Instance.AddCommand(command);
        }
    }
}
