using System;
using Spiff.IRC;
using Spiff.IRC.API.EventArgs;
using Spiffbot.Commands;

namespace Spiffbot
{
    class Program
    {
        private static TwitchIRC _server;
        static void Main(string[] args)
        {
            _server = new TwitchIRC("channel", "Username", "Password");

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
        }
    }
}
