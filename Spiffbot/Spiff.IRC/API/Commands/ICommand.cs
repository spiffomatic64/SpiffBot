using System.Linq;

namespace Spiff.Core.API.Commands
{
    public abstract class ICommand
    {
        public abstract string CommandName { get; }
        public abstract string CommandInfo { get; }

        //Methods
        public abstract void Run(string[] parts, string complete, string channel, string nick);

        protected bool IsMod(string nick)
        {
            var users = TwitchAPI.GetChatters(TwitchIRC.Instance.Channel);
            var user = (from s in users where s.Username == nick select s).FirstOrDefault();

            return user != null && user.IsMod;
        }
    }
}
