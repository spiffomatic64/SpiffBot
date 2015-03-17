using System;

namespace Spiff.Core.IRC
{
    public class TwitchEvent : EventArgs
    {
        public string Payload { get; private set; }

        public TwitchEvent(string payload)
        {
            Payload = payload;
        }
    }
}
