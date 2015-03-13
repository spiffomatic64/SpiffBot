using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Spiff.IRC;
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

            _server.Start();
        }

        static void LoadCommands()
        {
            _server.AddCommand(new HelpCommand());
            _server.AddCommand(new AllCommands());
        }
    }
}
