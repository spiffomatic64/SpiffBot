using System.Linq;
using Spiff.Core.API.Twitch;

namespace Spiff.Core.API.Commands
{
    public abstract class Command
    {
        public abstract string CommandName { get; }
        public abstract string CommandInfo { get; }

        //Methods
        public abstract void Run(string[] parts, string complete, string channel, string nick);

        protected bool IsMod(string nick)
        {
            var users = SiteApi.GetChatters(SpiffCore.Instance.Channel);
            var user = (from s in users where s.Username == nick select s).FirstOrDefault();

            return user != null && user.IsMod;
        }

        protected bool IsOwner(string nick)
        {
            return SpiffCore.Instance.Channel.ToLower().Equals(nick.ToLower());
        }

        protected SiteApi.Viewer GetViewer(string nick)
        {
            var users = SiteApi.GetChatters(SpiffCore.Instance.Channel);

            return (from s in users where s.Username.ToLower().Equals(nick.ToLower()) select s).FirstOrDefault();
        }

        protected void Boardcast(string message)
        {
            SpiffCore.Instance.WriteOut.SendMessage(message);
        }
    }
}
