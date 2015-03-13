using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using Spiff.IRC.API.Commands;

namespace Spiff.IRC
{
    public class TwitchIRC
    {
        //Public Vars
        public string Channel { get; private set; }
        public string BotName { get; private set; }
        public string BotPass { get; private set; }

        //Client vars
        private readonly TcpClient _client;
        private readonly NetworkStream _nwStream;
        private readonly StreamReader _reader;
        private readonly StreamWriter _writer;
        public OutUtils WriteOut { get; private set; }

        //Listen thread
        Thread listen;

        //Command List
        private Dictionary<string, ICommand> Commands;  

        //Instance
        private static TwitchIRC _instance;

        public static TwitchIRC Instance
        {
            get { return _instance; }
        }

        public TwitchIRC(string channel, string botName, string botPass)
        {
            Channel = channel;
            BotName = botName;
            BotPass = botPass;

             _client = new TcpClient("irc.twitch.tv", 6667);
            _nwStream = _client.GetStream();
            _reader = new StreamReader(_nwStream, Encoding.GetEncoding("iso8859-1"));
            _writer = new StreamWriter(_nwStream, Encoding.GetEncoding("iso8859-1"));

            WriteOut = new OutUtils(_writer);


        }

        public void Start()
        {
            listen = new Thread(Listener);
            listen.Start();

            Login();
        }

        public void AddCommand(ICommand command)
        {
            ICommand _command;
            Commands.TryGetValue("!" + command.CommandName, out _command);

            if (_command == null)
            {
                Commands.Add("!" + command.CommandName, command);
            }
        }

        public void RemoveCommand(ICommand command)
        {
            ICommand _command;
            Commands.TryGetValue("!" + command.CommandName, out _command);

            if (_command == null)
            {
                Commands.Remove("!" + command.CommandName);
            }
        }

        public void RemoveCommand(string command)
        {
            ICommand _command;
            Commands.TryGetValue("!" + command, out _command);

            if (_command == null)
            {
                Commands.Remove("!" + command);
            }
        }

        public Dictionary<string, ICommand> AllCommands()
        {
            return Commands;
        }

        private void Login()
        {
            WriteOut.SendCustom("USER " + BotName + "tmi twitch :" + BotName);
            WriteOut.SendCustom("PASS " + BotPass);
            WriteOut.SendCustom("NICK " + BotName);
        }

        private void Listener()
        {
            try
            {
                string data;
                while ((data = _reader.ReadLine()) != null)
                {
                    string _nick = "";
                    string _type = "";
                    string _channel = "";
                    string _message = "";

                    var ex = data.Split(new[] { ' ' }, 5);
                    if (ex[0] == "PING")
                    {
                        WriteOut.SendCustom("PONG " + ex[1]);
                    }

                    string[] split1 = data.Split(':');
                    if (split1.Length > 1)
                    {
                        //Splitting nick, type, chan and message
                        var split2 = split1[1].Split(' ');

                        //Nick consists of various things - we only want the nick itself
                        _nick = split2[0];
                        _nick = _nick.Split('!')[0];

                        //Type = PRIVMSG for normal messages. Only thing we need
                        _type = split2[1];

                        //Channel posted to
                        _channel = split2[2];

                        //Get message
                        if (split1.Length > 2)
                        {
                            for (var i = 2; i < split1.Length; i++)
                            {
                                _message += split1[i] + " ";
                            }
                        }

                        if (_message.StartsWith("!"))
                        {
                            ICommand _command;
                            Commands.TryGetValue(data.Split(' ')[0], out _command);

                            if (_command != null)
                            {
                                _command.Run(data.Split(' '), data, _channel, _nick);
                            }
                        }
                    }
                    Console.WriteLine(data);
                }
            }
            catch (Exception e)
            {
                listen.Abort();
            }
        }
    }
}
