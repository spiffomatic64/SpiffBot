using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using Spiff.Core.Extensions;
using Spiff.Core.Utils;

namespace Spiff.Core.API
{
    public class PluginLoader
    {
        private readonly string _directory;
        public List<Plugin> LoadedPlugins { get; private set; }
        public Dictionary<string, Assembly> LoadedAssemblies { get; private set; }


        public PluginLoader(string directory)
        {
            _directory = directory;

            LoadedPlugins = new List<Plugin>();
            LoadedAssemblies = new Dictionary<string, Assembly>();
        }

        public void LoadPlugins()
        {
            foreach (
                var assembly in
                    Directory.GetFiles(
                        _directory,
                        "*.dll").Select(Assembly.LoadFile))
            {
                AddAssembly(assembly);
                LoadPlugin(assembly);
            }
        }

        public void LoadPlugin(Assembly plugin, bool start = false)
        {
            if (plugin == null) return;
            var types = plugin.GetTypes();
            foreach (var pin in from type in types where !type.IsInterface && !type.IsAbstract where type.HasAbstract(typeof(Plugin)) select (Plugin)Activator.CreateInstance(type))
            {
                Logger.Info(string.Format("Loading Plugin - {0}(V -> {1})", pin.Name, pin.Version), "Plugin Engine");
                if (start)
                    pin.Start();
                LoadedPlugins.Add(pin);
                break;
            }
        }

        public void AddAssembly(Assembly asm)
        {
            if (!LoadedAssemblies.ContainsKey(asm.FullName))
                LoadedAssemblies.Add(asm.FullName, asm);
        }

        public Assembly GetAsm(string fullname)
        {
            Assembly asm;
            LoadedAssemblies.TryGetValue(fullname, out asm);
            return asm;
        }

        public Plugin GetPlugin(string name)
        {
            return (from s in LoadedPlugins where s.Name == name select s).FirstOrDefault();
        }

        public Plugin GetPlugin(Plugin plugin)
        {
            return (from s in LoadedPlugins where s == plugin select s).FirstOrDefault();
        }

        public void StartPlugins()
        {
            foreach (var plugin in LoadedPlugins)
            {
                plugin.Start();
            }
        }
    }
}
