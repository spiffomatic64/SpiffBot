using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Threading;
using Spiff.Core.API;
using Spiff.Core.API.Commands;
using Spiff.Core.API.EventArgs;
using Spiff.Core.Utils;

namespace Spiff.Core
{
    public class TwitchIRC
    {
        //Public Vars
        public string Channel { get; private set; }
        public string BotName { get; private set; }
        private string oauth { get; set; }

        //Client vars
        private readonly TcpClient _client;
        private readonly NetworkStream _nwStream;
        private readonly StreamReader _reader;
        private readonly StreamWriter _writer;
        public OutUtils WriteOut { get; private set; }

        //event Args
        public EventHandler<ChatEvent> OnChatHandler;

            //Listen thread
        Thread listen;

        //Command List
        private Dictionary<string, ICommand> Commands;
        private List<Plugin> BotPlugins = new List<Plugin>(); 

        //Instance
        public static TwitchIRC Instance { get; private set; }

        public TwitchIRC(string channel, string botName, string outh)
        {
            Channel = channel;
            BotName = botName;
            oauth = outh;

             _client = new TcpClient("irc.twitch.tv", 6667);
            _nwStream = _client.GetStream();
            _reader = new StreamReader(_nwStream, Encoding.GetEncoding("iso8859-1"));
            _writer = new StreamWriter(_nwStream, Encoding.GetEncoding("iso8859-1"));

            WriteOut = new OutUtils(_writer);

            Commands = new Dictionary<string, ICommand>();

            Instance = this;
        }

        public void Start()
        {
            listen = new Thread(Listener);
            listen.Start();

            Login();
            WriteOut.SendChannelJoin(Channel);
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

        public void LoadPlugin(Assembly plugin)
        {
            if (plugin != null)
            {
                Type[] types = plugin.GetTypes();
                foreach (Type type in types)
                {
                    if (!type.IsInterface && !type.IsAbstract)
                    {
                        if (type.IsSubclassOf(typeof(Plugin)))
                        {
                            Plugin pin = (Plugin) Activator.CreateInstance(type);
                            Console.WriteLine("[" + pin.Name + "]Loading Plugin");
                            pin.Start();
                            BotPlugins.Add(pin);
                            break;
                        }
                    }
                }
            } 
        }

        private void Login()
        {
            WriteOut.SendCustom("PASS oauth:" + oauth);
            WriteOut.SendCustom("NICK " + BotName);
            WriteOut.SendCustom("USER " + BotName + " :SpiffBot");
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

                    Console.WriteLine(data);
                    var ex = data.Split(new[] { ' ' }, 5);
                    if (ex[0] == "PING")
                    {
                        WriteOut.SendCustom("PONG " + ex[1]);
                        continue;
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

                        if (_type == "PRIVMSG" && _channel.Contains("#"))
                        {
                            if (OnChatHandler != null)
                            {
                                OnChatHandler(this, new ChatEvent(_channel, _nick, _message));
                            }
                        }

                        if (_message.StartsWith("!"))
                        {
                            //Console.WriteLine(_message.Split(' ')[0]);
                            ICommand _command;
                            Commands.TryGetValue(_message.Split(' ')[0], out _command);

                            if (_command != null)
                            {
                                _command.Run(_message.Split(new[] {' '}, StringSplitOptions.RemoveEmptyEntries), _message, _channel.TrimStart('#'), _nick);
                            }
                        }
                    }
                    //Console.WriteLine(data);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                Console.ReadKey();
                //listen.Abort();
            }
        }
    }
}
