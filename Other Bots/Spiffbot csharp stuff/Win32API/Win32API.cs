using Spiff.Core.API;
using Spiff.Core.Utils;

namespace Win32API
{
    public class Win32API : Plugin
    {
        public override string Name
        {
            get { return "Win32API"; }
        }

        public override string Author
        {
            get { return "Toyz"; }
        }

        public override string Description
        {
            get { return "Win32API binding for C# that can be access in GetPlugin"; }
        }

        public override int Version
        {
            get { return 1; }
        }

        public override void Start()
        {
            Logger.Info("Loaded Win32API Bindings", Name);
        }

        public override void Destory()
        {
            //throw new NotImplementedException();
        }
    }
}
