using System.Collections.Generic;
using System.Linq;
using Spiff.Core;
using Spiff.Core.API.Commands;

namespace DefaultCommands.Commands
{
    public class PluginsCommand : Command
    {
        public override string CommandName
        {
            get { return "plugins";  }
        }

        public override string CommandInfo
        {
            get { return "A list of all loaded plugins"; }
        }

        public override void Run(string[] parts, string complete, string channel, string nick)
        {
            List<string> pluginNames = SpiffCore.Instance.PluginLoader.LoadedPlugins.Select(plugin => plugin.Name).ToList();

            Boardcast(string.Format("Loaded Plugins({0}): {1}", pluginNames.Count, string.Join(", ", pluginNames)));
        }
    }
}
