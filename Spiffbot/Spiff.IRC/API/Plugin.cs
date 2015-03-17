using System.IO;
using System.Linq;
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
        public abstract int Version { get; }

        //Abstracts
        public void Preload()
        {
            //Can be overried to Preload stuff  
        }
        public abstract void Start();
        public abstract void Destory();

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
        public SpiffCore SpiffCore
        {
            get { return SpiffCore.Instance; }
        }
        public OutUtils Writer
        {
            get { return SpiffCore.WriteOut; }
        }

        public string PluginDirectory
        {
            get
            {
                if (!Directory.Exists(Path.Combine("Plugins", Name)))
                {
                    Directory.CreateDirectory(Path.Combine("Plugins", Name));
                }
                return Path.Combine("Plugins", Name);
            }
        }

        protected void RegisterCommand(Command command)
        {
            SpiffCore.Instance.AddCommand(command);
        }

        protected Plugin GetPlugin(string name)
        {
            return SpiffCore.PluginLoader.GetPlugin(name);
        }

        protected Plugin GetPlugin(Plugin plugin)
        {
            return SpiffCore.PluginLoader.GetPlugin(plugin);
        }
    }
}
