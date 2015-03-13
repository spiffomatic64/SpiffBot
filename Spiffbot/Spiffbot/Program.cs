using System;
using System.IO;
using System.Reflection;
using Spiff.Core;
using Spiff.Core.API.Config;
using Spiff.Core.API.EventArgs;

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

            _server = new TwitchIRC(ConfigFile.GetValue("channel", "channel", "thetoyz"), ConfigFile.GetValue("auth", "Username", "ToyzBot"), ConfigFile.GetValue("auth", "oauth", "oauth"));

            LoadPlugins();
            _server.OnChatHandler += OnChatHandler;
            _server.Start();
        }

        private static void OnChatHandler(object sender, ChatEvent chatEvent)
        {
            Console.WriteLine("[Chat][" + chatEvent.Channel + "]" + chatEvent.User + ": " + chatEvent.Message);
        }

        static void LoadPlugins()
        {
            foreach (var dll in Directory.GetFiles(Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "Plugins"), "*.dll"))
            {
                Console.WriteLine(dll);
                Assembly assembly = Assembly.LoadFile(dll);
                TwitchIRC.Instance.LoadPlugin(assembly);
            }
        }
    }
}
