using System;
using System.IO;
using System.Reflection;
using System.Threading;
using Spiff.Core;
using Spiff.Core.API;
using Spiff.Core.API.Twitch;
using Spiff.Core.IRC;
using Spiff.Core.Utils;

namespace Spiffbot
{
    class Program
    {
        private static SpiffCore _server;
        private static readonly Ini ConfigFile = new Ini("Config.ini");
        private static bool Stopping = false;

        static void Main(string[] args)
        {
            if (!Directory.Exists("Plugins"))
                Directory.CreateDirectory("Plugins");

            if (!File.Exists("Config.ini"))
            {
                ConfigFile.SetValue("auth", "Username", "ToyzBot");
                ConfigFile.SetValue("auth", "oauth", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
                ConfigFile.SetValue("channel", "channel", "thetoyz");
                ConfigFile.SetValue("adv", "debug", false);
                ConfigFile.Flush();

                Logger.Info("...SpiffBot...", "SpiffBot");
                Logger.Error("Please Edit Config.ini with your settings...", "SpiffBot");

                Console.ReadKey();
                Environment.Exit(0);
            }

            string pluginPath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "Plugins");
            Logger.Info("Please Wait... Spiffbot is loading...", "SpiffBot");
            _server = new SpiffCore(ConfigFile.GetValue("channel", "channel", "thetoyz"), ConfigFile.GetValue("auth", "Username", "ToyzBot"), ConfigFile.GetValue("auth", "oauth", "oauth"), pluginPath);

            Logger.Info("Loading all plugins", "SpiffBot");
            SpiffCore.Instance.PluginLoader.LoadPlugins();
            SpiffCore.Instance.PluginLoader.StartPlugins();
            Logger.Info("Plugins have been loaded", "SpiffBot");
            _server.IrcClient.OnTwitchDataDebugOut += IrcClientOnOnTwitchDataDebugOut;
            _server.IrcClient.Start();

            new Thread(TitleUpdater).Start();
            Logger.Info("Spiffbot has started and conntected to twitch", "SpiffBot");

            Console.CancelKeyPress += ConsoleOnCancelKeyPress;
        }

        private static void ConsoleOnCancelKeyPress(object sender, ConsoleCancelEventArgs consoleCancelEventArgs)
        {
            Stopping = true;

            Logger.Info("SpiffBot is shutting down", "SpiffBot");
            foreach (var plugin in SpiffCore.Instance.PluginLoader.LoadedPlugins)
            {
                plugin.Destory();
            }

            SpiffCore.Instance.IrcClient.ServerThread().Abort();
        }

        private static void IrcClientOnOnTwitchDataDebugOut(object sender, TwitchEvent twitchEvent)
        {
            if (ConfigFile.GetValue("adv", "debug", false))
            {
                Logger.Debug(twitchEvent.Payload, "Debug");
            }
        }

        private static void TitleUpdater()
        {
            while (!Stopping)
            {
                var viewers = SiteApi.GetChatters(SpiffCore.Instance.Channel).Count;

                Console.Title = string.Format("Spiffbaot - Viewers: {0}", viewers);

                Thread.Sleep(1000);
            }
        }
    }
}
