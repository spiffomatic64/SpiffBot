using System.IO;

namespace Spiff.IRC
{
    public class OutUtils
    {
        private readonly StreamWriter _writer;

        public OutUtils(StreamWriter writer)
        {
            _writer = writer;
        }

        public void SendMessage(string message, string channel)
        {
            _writer.WriteLine("PRIVMSG #{0} :{1}", channel, message);
            _writer.Flush();
        }

        public void SendChannelJoin(string channel)
        {
            _writer.WriteLine("PRIVMSG #{0}", channel);
            _writer.Flush();
        }

        public void SendCustom(string command)
        {
            _writer.WriteLine(command);
            _writer.Flush();
        }
    }
}
