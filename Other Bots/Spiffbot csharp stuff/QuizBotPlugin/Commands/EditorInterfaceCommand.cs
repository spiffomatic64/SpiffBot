using System.Threading;
using System.Windows.Forms;
using QuizBotPlugin.Forms;
using Spiff.Core.API.Commands;

namespace QuizBotPlugin.Commands
{
    public class EditorInterfaceCommand : Command
    {
        public override string CommandName
        {
            get { return "quizeditor"; }
        }

        public override string CommandInfo
        {
            get { return "This allows the chat owner to add custom quiz/edit current ones"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            if (IsOwner(nick))
            {
                var t = new Thread(() => { Application.Run(new QuizBuilder()); });

                t.SetApartmentState(ApartmentState.STA);
                t.Start();
            }
        }
    }
}
