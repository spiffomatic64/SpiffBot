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
        private string Oauth { get; set; }

        //Client vars
        private readonly StreamReader _reader;
        public OutUtils WriteOut { get; private set; }

        //event Args
        public event EventHandler<ChatEvent> OnChatHandler;
        public event EventHandler<OnCommandEvent> OnCommandHandler;

        //Listen thread
        Thread _listen;

        //Command List
        public Dictionary<string, ICommand> Commands {get; private set; }
        public List<Plugin> BotPlugins {get; private set;}

        //Instance
        public static TwitchIRC Instance { get; private set; }

        public TwitchIRC(string channel, string botName, string outh)
        {
            Channel = channel;
            BotName = botName;
            Oauth = outh;

             var client = new TcpClient("irc.twitch.tv", 6667);
            var nwStream = client.GetStream();
            _reader = new StreamReader(nwStream, Encoding.GetEncoding("iso8859-1"));
            var writer = new StreamWriter(nwStream, Encoding.GetEncoding("iso8859-1"));

            WriteOut = new OutUtils(writer);

            Commands = new Dictionary<string, ICommand>();
            BotPlugins = new List<Plugin>();

            Instance = this;
        }

        #region Publics
        public void Start()
        {
            _listen = new Thread(Listener);
            _listen.Start();

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

        public List<Plugin> AllPlugins()
        {
            return BotPlugins;
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
        #endregion

        #region Privates
        private void Login()
        {
            WriteOut.SendCustom("PASS oauth:" + Oauth);
            WriteOut.SendCustom("NICK " + BotName);
            WriteOut.SendCustom("USER " + BotName + " :SpiffBot");
        }

        protected virtual void Listener()
        {
            try
            {
                string data;
                while ((data = _reader.ReadLine()) != null)
                {
                    string message = "";

                    Console.WriteLine(data);
                    var ex = data.Split(new[] {' '}, 5);
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
                        var nick = split2[0];
                        nick = nick.Split('!')[0];

                        //Type = PRIVMSG for normal messages. Only thing we need
                        var type = split2[1];

                        //Channel posted to
                        var channel = split2[2];

                        //Get message
                        if (split1.Length > 2)
                        {
                            for (var i = 2; i < split1.Length; i++)
                            {
                                message += split1[i] + " ";
                            }
                        }

                        if (type == "PRIVMSG" && channel.Contains("#"))
                        {
                            if (OnChatHandler != null)
                                OnChatHandler(this, new ChatEvent(channel, nick, message));
                        }

                        if (message.StartsWith("!"))
                        {
                            //Console.WriteLine(_message.Split(' ')[0]);
                            ICommand command;
                            Commands.TryGetValue(message.Split(' ')[0], out command);

                            if (command != null)
                            {
                                var args = message.Split(new[] {' '}, StringSplitOptions.RemoveEmptyEntries);
                                if (OnCommandHandler != null)
                                    OnCommandHandler(this, new OnCommandEvent(command, args, message));

                                command.Run(args, message, channel.TrimStart('#'), nick);
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
        #endregion
    }
}
