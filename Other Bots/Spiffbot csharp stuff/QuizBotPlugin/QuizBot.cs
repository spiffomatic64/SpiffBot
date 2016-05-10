using QuizBotPlugin.Commands;
using Spiff.Core.API;

namespace QuizBotPlugin
{
    public class QuizBot : Plugin
    {
        public override string Name
        {
            get { return "QuizBot"; }
        }
        public override string Author
        {
            get { return "Toyz"; }
        }
        public override string Description
        {
            get { return "A very simple quizbot to test the chat handlers"; }
        }
        public override int Version
        {
            get { return 1; }
        }

        public static QuizBot BotInstance { get; private set; }
        public override void Start()
        {
            BotInstance = this;

            RegisterCommand(new EditorInterfaceCommand());
            RegisterCommand(new StartQuizCommand());
        }

        public override void Destory()
        {
            //throw new NotImplementedException();
        }
    }
}
