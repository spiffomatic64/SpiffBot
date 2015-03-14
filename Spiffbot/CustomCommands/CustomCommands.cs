using System.IO;
using CustomCommands.Commands;
using Spiff.Core.API;
using Spiff.Core.Utils;

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

        public override int Version
        {
            get { return 1; }
        }

        public static Ini ConfigSettings;
        public override void Start()
        {
            ConfigSettings = Config;
            if (!File.Exists(Config.FileName))
            {
                ConfigSettings.SetValue("config", "Song_File", "c:\\Path\\To\\Song");
                ConfigSettings.Flush();
            }

            Logger.Debug("Is Default Plugin Set: " + ((DefaultCommands.DefaultCommands)GetPlugin("Default Commands") != null), Name);
            RegisterCommand(new SourceCommand());
            RegisterCommand(new SongCommand());
            RegisterCommand(new ReloadConfigSettings());
        }

        public override void Destory()
        {
            
        }
    }
}
