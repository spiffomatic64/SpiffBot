using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using Spiff.Core.Utils;

namespace Spiff.Core.IRC
{
    public class IRCClient
    {
        private readonly string _channel;
        private readonly string _user;
        private readonly string _oauth;
        private readonly SpiffCore _twitch;

        private Thread _serverThread;
        private StreamReader _reader;
        private StreamWriter _streamWriter;

        public event EventHandler<TwitchEvent> OnTwitchEvent;
        public event EventHandler<TwitchEvent> OnTwitchDataDebugOut;

        public IRCClient(string channel, string user, string oauth, SpiffCore twitch)
        {
            _channel = channel;
            _user = user;
            _oauth = oauth;
            _twitch = twitch;
        }

        public void Start()
        {
            Setup();
            Startup();
            Login();
        }

        public Thread ServerThread()
        {
            return _serverThread;
        }

        private void Setup()
        {
            var client = new TcpClient("irc.twitch.tv", 6667);
            var nwStream = client.GetStream();
            _reader = new StreamReader(nwStream, Encoding.GetEncoding("iso8859-1"));
            _streamWriter = new StreamWriter(nwStream, Encoding.GetEncoding("iso8859-1"));

            _twitch.WriteOut = new OutUtils(_streamWriter, _channel);
        }

        private void Startup()
        {
            _serverThread = new Thread(Listener);
            _serverThread.Start();
        }

        public void Login()
        {
            var writeOut = _twitch.WriteOut;

            writeOut.SendCustom("PASS oauth:" + _oauth);
            writeOut.SendCustom("NICK " + _user);
            writeOut.SendCustom("USER " + _user + " :SpiffBot");
            writeOut.SendChannelJoin();
        }

        private void Listener()
        {
            var writeOut = _twitch.WriteOut;
            string data;
            while ((data = _reader.ReadLine()) != null)
            {
                var ex = data.Split(new[] { ' ' }, 5);
                if (ex[0] == "PING")
                {
                    writeOut.SendCustom("PONG " + ex[1]);
                    continue;
                }

                if(OnTwitchEvent != null)
                    OnTwitchEvent(this, new TwitchEvent(data));

                if (OnTwitchDataDebugOut != null)
                    OnTwitchDataDebugOut(this, new TwitchEvent(data));
            }
        }
    }
}
