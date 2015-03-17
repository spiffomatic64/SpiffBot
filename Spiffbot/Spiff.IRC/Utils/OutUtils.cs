using System;
using System.IO;

namespace Spiff.Core.Utils
{
    public class OutUtils
    {
        private readonly StreamWriter _writer;
        private readonly string _channel;

        public OutUtils(StreamWriter writer, string channel)
        {
            if (writer == null) throw new ArgumentNullException("writer");
            if (channel == null) throw new ArgumentNullException("channel");
            _writer = writer;
            _channel = channel;
        }

        public void SendMessage(string message)
        {
            _writer.WriteLine("PRIVMSG #{0} :{1}", _channel, message);
            _writer.Flush();
        }

        public void SendChannelJoin()
        {
            _writer.WriteLine("JOIN #{0}", _channel);
            _writer.Flush();
        }

        public void TimeoutUser(string user, int timeout = 600)
        {
            SendMessage(string.Format("/timeout {0} {1}", user, timeout));
        }

        public void BanUser(string user)
        {
            SendMessage(string.Format("/ban {0}", user));
        }

        public void UnbanUser(string user)
        {
            SendMessage(string.Format("/unban {0}", user));
        }

        public void SendCustom(string command)
        {
            _writer.WriteLine(command);
            _writer.Flush();
        }
    }
}
