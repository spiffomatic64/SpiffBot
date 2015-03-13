namespace Spiff.Core.API.EventArgs
{
    public class ChatEvent : System.EventArgs
    {
        public string Channel { get; private set; }
        public string User { get; private set; }
        public string Message { get; private set; }

        public ChatEvent(string channel, string user, string message)
        {
            Channel = channel;
            User = user;
            Message = message;
        }
    }
}
