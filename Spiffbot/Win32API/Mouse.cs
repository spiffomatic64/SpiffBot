using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Win32API
{
    public static class Mouse
    {
        public static void Move(int x, int y)
        {
            Invoke.POINT p = new Invoke.POINT {x = x, y = y};

            if (System.Windows.Forms.Cursor.Current != null)
                Invoke.ClientToScreen(System.Windows.Forms.Cursor.Current.Handle, ref p);
            Invoke.SetCursorPos(p.x, p.y);
        }
    }
}
