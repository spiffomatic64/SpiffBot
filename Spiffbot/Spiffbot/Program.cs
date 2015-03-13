using System;
using Spiff.Core;
using Spiff.Core.API.Config;
using Spiff.Core.API.EventArgs;
using Spiffbot.Commands;

namespace Spiffbot
{
    class Program
    {
        private static TwitchIRC _server;
        private static readonly Ini ConfigFile = new Ini("Config.ini");
        static void Main(string[] args)
        {
            _server = new TwitchIRC(ConfigFile.GetValue("channel", "channel", "thetoyz"), ConfigFile.GetValue("auth", "Username", "ToyzBot"), ConfigFile.GetValue("auth", "oauth", "oauth"));

            LoadCommands();
            _server.OnChatHandler += OnChatHandler;
            _server.Start();
        }

        private static void OnChatHandler(object sender, ChatEvent chatEvent)
        {
            Console.WriteLine("[Chat][" + chatEvent.Channel + "]" + chatEvent.User + ": " + chatEvent.Message);
        }

        static void LoadCommands()
        {
            _server.AddCommand(new HelpCommand());
            _server.AddCommand(new AllCommands());
            _server.AddCommand(new GameCommand());
        }
    }
}
