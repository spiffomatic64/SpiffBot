using Spiff.Core.API.Commands;

namespace QuizBotPlugin.Commands
{
    public class StartQuizCommand : Command
    {
        public override string CommandName
        {
            get { return "startquiz"; }
        }

        public override string CommandInfo
        {
            get { return "Command to start a give quiz"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            if (IsOwner(nick))
            {
               new QuizMaster(parts[1] + ".xml");
            }
        }
    }
}
