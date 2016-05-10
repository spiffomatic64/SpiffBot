namespace Spiff.Core.API.EventArgs
{
    public class OnUserLeftEvent : System.EventArgs
    {
        public string Channel { get; private set; }
        public string Nick { get; private set; }

        public OnUserLeftEvent(string nick, string channel)
        {
            Channel = channel;
            Nick = nick;
        }
    }
}
