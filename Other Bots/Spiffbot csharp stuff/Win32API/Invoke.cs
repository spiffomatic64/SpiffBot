using System;
using System.Runtime.InteropServices;

namespace Win32API
{
    public static class Invoke
    {

        //Mouse Move
        [DllImport("User32.Dll")]
        public static extern long SetCursorPos(int x, int y);

        [DllImport("User32.Dll")]
        public static extern bool ClientToScreen(IntPtr hWnd, ref POINT point);

        [StructLayout(LayoutKind.Sequential)]
        public struct POINT
        {
            public int x;
            public int y;
        }

        //Monitor control
        public static int WM_SYSCOMMAND = 0x0112;
        public static int SC_MONITORPOWER = 0xF170; 

        [DllImport("user32.dll")]
        private static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);
    }
}
