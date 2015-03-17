using System.Windows.Forms;

namespace Win32API
{
    public static class Mouse
    {
        public static void Move(int x, int y)
        {
            Invoke.POINT p = new Invoke.POINT {x = x, y = y};

            if (Cursor.Current != null)
                Invoke.ClientToScreen(Cursor.Current.Handle, ref p);
            Invoke.SetCursorPos(p.x, p.y);
        }
    }
}
