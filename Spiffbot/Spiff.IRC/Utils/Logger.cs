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

        public static void Error(Object error)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine(error);
            Console.ForegroundColor = OrginalColor;
        }

        public static void Info(Object info)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine(info);
            Console.ForegroundColor = OrginalColor;
        }

        public static void Debug(Object debug)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine(debug);
            Console.ForegroundColor = OrginalColor;
        }

        public static void Write(Object write)
        {
            Console.ForegroundColor = OrginalColor;
            Console.WriteLine(write);
            Console.ForegroundColor = OrginalColor;
        }
    }
}
