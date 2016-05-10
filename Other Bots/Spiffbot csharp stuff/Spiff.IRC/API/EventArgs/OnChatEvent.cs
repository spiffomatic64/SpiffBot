namespace Spiff.Core.API.EventArgs
{
    public class OnChatEvent : System.EventArgs
    {
        public string Channel { get; private set; }
        public string User { get; private set; }
        public string Message { get; private set; }

        public OnChatEvent(string channel, string user, string message)
        {
            Channel = channel;
            User = user;
            Message = message;
        }
    }
}
