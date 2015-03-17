using System;
using System.Collections;
using System.Runtime.InteropServices;
using System.Threading;

namespace MDXInfo.DirectX.XInput
{
    public enum ControllerButtons : ushort
    {
        Up = 0x00000001,
        Down = 0x00000002,
        Left = 0x00000004,
        Right = 0x00000008,
        Start = 0x00000010,
        Back = 0x00000020,
        ThumbLeft = 0x00000040,
        ThumbRight = 0x00000080,
        ShoulderLeft = 0x0100,
        ShoulderRight = 0x0200,
        A = 0x1000,
        B = 0x2000,
        X = 0x4000,
        Y = 0x8000,

        None = 0
    }

    [StructLayout(LayoutKind.Sequential)]
    internal struct Vibration
    {
        public ushort LeftMotorSpeed;
        public ushort RightMotorSpeed;

        public Vibration(ushort left, ushort right)
        {
            LeftMotorSpeed = left;
            RightMotorSpeed = right;
        }
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct GamePad
    {
        public ControllerButtons Buttons;
        public byte LeftTrigger;
        public byte RightTrigger;
        public short ThumbLeftX;
        public short ThumbLeftY;
        public short ThumbRightX;
        public short ThumbRightY;

        public override bool Equals(object o)
        {
            if (o is GamePad)
            {
                GamePad gp = (GamePad)o;

                return gp.Buttons == this.Buttons &&
                    gp.LeftTrigger == this.LeftTrigger &&
                    gp.RightTrigger == this.RightTrigger &&
                    gp.ThumbLeftX == this.ThumbLeftX &&
                    gp.ThumbLeftY == this.ThumbLeftY &&
                    gp.ThumbRightX == this.ThumbRightX &&
                    gp.ThumbRightY == this.ThumbRightY;
            }
            else
            {
                return false;
            }
        }

        public override int GetHashCode()
        {
            return ((int)this.Buttons) ^ LeftTrigger ^ RightTrigger ^ ThumbLeftX ^ ThumbLeftY ^ ThumbRightX ^ ThumbRightY;
        }
    }


    [StructLayout(LayoutKind.Sequential)]
    public struct State
    {
        public uint PacketNumber;
        public GamePad Gamepad;

        public override bool Equals(object o)
        {
            if (o is State)
            {
                State s = (State)o;
                return this.Gamepad.Equals(s.Gamepad);
            }
            else
            {
                return false;
            }
        }

        public override int GetHashCode()
        {
            return this.Gamepad.GetHashCode();
        }
    }


    public class ControllerCollection
    {
        private ArrayList controllers = new ArrayList();

        public ControllerCollection()
        {
            for (int i = 0; i < 4; i++)
            {
                controllers.Add(new Controller(i));
            }
        }

        public Controller this[int index]
        {
            get
            {
                return (Controller)this.controllers[index];
            }
        }
    }

    public class XInput
    {
        public const int ERROR_SUCCESS = 0;
        private static Thread pollThread;

        // internal poll interval in ms
        private static int pollInterval = 20;
        private static bool eventModelEnabled = true;

        public static bool EventModelEnabled
        {
            get { return XInput.eventModelEnabled; }
            set { XInput.eventModelEnabled = value; }
        }



        static XInput()
        {
            pollThread = new Thread(new ThreadStart(PollForEvents));
            pollThread.Name = "MDXInfo.DirectX.XInput event thread";
            pollThread.IsBackground = true;
            pollThread.Start();
        }

        private XInput()
        {
            // no instanciation			
        }


        private static ControllerCollection controllerList = new ControllerCollection();
        public static ControllerCollection Controllers
        {
            get { return controllerList; }
        }

        private static void PollForEvents()
        {
            while (true)
            {
                if (EventModelEnabled)
                {
                    for (int i = 0; i < 4; i++)
                    {
                        Controllers[i].PollForEvents();
                    }

                    Thread.Sleep(pollInterval);
                }
                else
                {
                    Thread.Sleep(250);
                }
            }
        }


        [System.Security.SuppressUnmanagedCodeSecurity] // We won't use this maliciously
        [DllImport("xinput9_1_0.dll", EntryPoint = "XInputSetState", CharSet = CharSet.Auto, CallingConvention = CallingConvention.Winapi)]
        internal static extern int SetState(int dwUserIndex, ref Vibration pVibration);


        [System.Security.SuppressUnmanagedCodeSecurity] // We won't use this maliciously
        [DllImport("xinput9_1_0.dll", EntryPoint = "XInputGetState", CharSet = CharSet.Auto, CallingConvention = CallingConvention.Winapi)]
        internal static extern int GetState(int dwUserIndex, ref State pState);


    }
}
