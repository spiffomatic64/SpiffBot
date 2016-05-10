namespace Spiff.Core.API.EventArgs
{
    public class OnUserJoinEvent : System.EventArgs
    {
        public string Nick { get; private set; }
        public string Channel { get; private set; }

        public OnUserJoinEvent(string nick, string channel)
        {
            Nick = nick;
            Channel = channel;
        }
    }
}
