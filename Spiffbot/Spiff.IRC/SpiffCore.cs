using System;
using System.Collections.Generic;
using System.Reflection;
using Spiff.Core.API;
using Spiff.Core.API.Commands;
using Spiff.Core.API.EventArgs;
using Spiff.Core.IRC;
using Spiff.Core.Utils;

namespace Spiff.Core
{
    public class SpiffCore
    {
        //Public Vars
        public string Channel { get; private set; }
        public string BotName { get; private set; }

        //Client vars
        public OutUtils WriteOut { get; set; }

        //event Args
        public event EventHandler<OnUserJoinEvent> OnUserJoinHandler;
        public event EventHandler<OnUserLeftEvent> OnUserLeftHandler;
        public event EventHandler<OnChatEvent> OnChatHandler;
        public event EventHandler<OnCommandEvent> OnCommandHandler;

        //Command List
        public Dictionary<string, Command> Commands {get; private set; }
        public PluginLoader PluginLoader { get; private set; }
        //Instance
        public static SpiffCore Instance { get; private set; }

        //Server IRC stuff
        public IRCClient IrcClient;

        public SpiffCore(string channel, string botName, string outh, string pluginDirectory)
        {
            Channel = channel;
            BotName = botName;
            PluginLoader = new PluginLoader(pluginDirectory);

            Commands = new Dictionary<string, Command>();

            Instance = this;

            IrcClient = new IRCClient(channel, botName, outh, this);

            IrcClient.OnTwitchEvent += IrcClientOnOnTwitchEvent;

            AppDomain.CurrentDomain.AssemblyResolve += CurrentDomainOnAssemblyResolve;
        }

        private Assembly CurrentDomainOnAssemblyResolve(object sender, ResolveEventArgs args)
        {
            //Nasty hack to fix talking between plugins but works the best maybe will find a better way later
            return PluginLoader.GetAsm(args.Name);
        }

        #region Publics
        public void AddCommand(Command command)
        {
            Command outcommand;
            Commands.TryGetValue("!" + command.CommandName, out outcommand);

            if (outcommand == null)
            {
                Commands.Add("!" + command.CommandName, command);
            }
        }

        public void RemoveCommand(Command command)
        {
            Command outcommand;
            Commands.TryGetValue("!" + command.CommandName, out outcommand);

            if (outcommand == null)
            {
                Commands.Remove("!" + command.CommandName);
            }
        }

        public void RemoveCommand(string command)
        {
            Command outcommand;
            Commands.TryGetValue("!" + command, out outcommand);

            if (outcommand == null)
            {
                Commands.Remove("!" + command);
            }
        }

        public Dictionary<string, Command> AllCommands()
        {
            return Commands;
        }

        #endregion

        #region Privates
        private void IrcClientOnOnTwitchEvent(object sender, TwitchEvent twitchEvent)
        {
            var data = twitchEvent.Payload;
            var message = "";

            var split1 = data.Split(':');
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

                if (split1.Length > 2)
                {
                    for (var i = 2; i < split1.Length; i++)
                    {
                        message += split1[i] + " ";
                    }
                }

                switch (type)
                {
                    case "PRIVMSG":
                        if (channel.StartsWith("#"))
                            if (OnChatHandler != null)
                                OnChatHandler(this, new OnChatEvent(channel, nick, message));
                        Logger.Info(string.Format("{0} -> {1}", nick, message), "Chat");
                        break;
                    case "JOIN":
                        if (channel.StartsWith("#"))
                            if (OnUserJoinHandler != null)
                                OnUserJoinHandler(this, new OnUserJoinEvent(nick, channel));
                        Logger.Info(string.Format("{0} has joined the chat", nick), "Joined Chat");
                        break;
                    case "PART":
                        if (channel.StartsWith("#"))
                            if (OnUserLeftHandler != null)
                                OnUserLeftHandler(this, new OnUserLeftEvent(nick, channel));
                        Logger.Info(string.Format("{0} has left the chat", nick), "Left Chat");
                        break;
                }

                if (message.StartsWith("!"))
                {
                    Command command;
                    Commands.TryGetValue(message.Split(' ')[0], out command);

                    if (command != null)
                    {
                        var args = message.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                        //try
                        //{
                            if (OnCommandHandler != null)
                                OnCommandHandler(this, new OnCommandEvent(command, args, message));

                            command.Run(args, message, channel.TrimStart('#'), nick);
                        /*}
                        catch (Exception ex)
                        {
                            RemoveCommand(command);
                            Logger.Error("Error in Running Command: " + ex, "Plugin Command Error");
                        }*/
                    }
                }
            }
        }
        #endregion
    }
}
