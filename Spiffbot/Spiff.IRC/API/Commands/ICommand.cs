namespace Spiff.IRC.API.Commands
{
    public abstract class ICommand
    {
        public abstract string CommandName { get; }
        public abstract string CommandInfo { get; }

        //Methods
        public abstract void Run(string[] parts, string complete, string channel, string nick);
    }
}
