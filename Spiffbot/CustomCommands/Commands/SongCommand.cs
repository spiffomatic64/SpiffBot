using System.IO;
using Spiff.Core.API.Commands;

namespace CustomCommands.Commands
{
    public class SongCommand : ICommand
    {
        public override string CommandName
        {
            get { return "song"; }
        }

        public override string CommandInfo
        {
            get { return "Get the current playing song"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            var file = CustomCommands.ConfigSettings.GetValue("config", "Song_File", "c:\\Path\\To\\Song");

            if (File.Exists(file))
            {
                Boardcast(string.Format("Hey, {0} the current song is: {1}", nick, File.ReadAllText(file)));
            }
        }
    }
}
