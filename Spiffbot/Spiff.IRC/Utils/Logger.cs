using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Spiff.Core.Utils
{
    public static class Logger
    {
        private static readonly ConsoleColor OrginalColor;
        static Logger()
        {
            OrginalColor = Console.ForegroundColor;
        }

        public static void Error(Object error, string from = "")
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine(string.IsNullOrWhiteSpace(from) ? error : string.Format("[{0}]{1}", @from, error));
            Console.ForegroundColor = OrginalColor;
        }

        public static void Info(Object info, string from = "")
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine(string.IsNullOrWhiteSpace(from) ? info : string.Format("[{0}]{1}", @from, info));
            Console.ForegroundColor = OrginalColor;
        }

        public static void Debug(Object debug, string from = "")
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine(string.IsNullOrWhiteSpace(from) ? debug : string.Format("[{0}]{1}", @from, debug));
            Console.ForegroundColor = OrginalColor;
        }

        public static void Write(Object write, string from = "")
        {
            Console.ForegroundColor = OrginalColor;
            Console.WriteLine(string.IsNullOrWhiteSpace(from) ? write : string.Format("[{0}]{1}", @from, write));
            Console.ForegroundColor = OrginalColor;
        }
    }
}
