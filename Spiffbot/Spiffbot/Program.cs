using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Threading;
using Spiff.Core;
using Spiff.Core.API.EventArgs;
using Spiff.Core.IRC;
using Spiff.Core.Utils;

namespace Spiffbot
{
    class Program
    {
        private static TwitchIRC _server;
        private static readonly Ini ConfigFile = new Ini("Config.ini");
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

                Logger.Error("Please Edit Config.ini with your settings...");

                Console.ReadKey();
                Environment.Exit(0);
            }

            Logger.Debug(ConfigFile.GetValue("adv", "debug", false));
            _server = new TwitchIRC(ConfigFile.GetValue("channel", "channel", "thetoyz"), ConfigFile.GetValue("auth", "Username", "ToyzBot"), ConfigFile.GetValue("auth", "oauth", "oauth"));

            LoadPlugins();
            _server.OnChatHandler += OnChatHandler;
            _server.IrcClient.OnTwitchDataDebugOut += IrcClientOnOnTwitchDataDebugOut;
            _server.IrcClient.Start();

            new Thread(TitleUpdater).Start();
        }

        private static void IrcClientOnOnTwitchDataDebugOut(object sender, TwitchEvent twitchEvent)
        {
            if (ConfigFile.GetValue("adv", "debug", false))
            {
                Logger.Debug("[Debug]" + twitchEvent.Payload);
            }
        }

        private static void OnChatHandler(object sender, OnChatEvent chatEvent)
        {
            Logger.Write("[Chat][" + chatEvent.Channel + "]" + chatEvent.User + ": " + chatEvent.Message);
        }

        static void LoadPlugins()
        {
            foreach (var assembly in Directory.GetFiles(Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "Plugins"), "*.dll").Select(dll => Assembly.LoadFile(dll)))
            {
                TwitchIRC.Instance.LoadPlugin(assembly);
            }

            TwitchIRC.Instance.StartPlugins();
        }

        static void TitleUpdater()
        {
            while (true)
            {
                var viewers = TwitchAPI.GetChatters(TwitchIRC.Instance.Channel).Count;

                Console.Title = string.Format("Spiffbot - Viewers: {0}", viewers);

                Thread.Sleep(1000);
            }
        }
    }
}
