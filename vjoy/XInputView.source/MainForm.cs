using System;
using System.IO;
using System.IO.Pipes;
using System.Reflection;
using System.Drawing;
using System.Collections;
using System.ComponentModel;
using System.Windows.Forms;
using System.Data;
using System.Runtime.InteropServices;

using MDXInfo.DirectX.XInput;
using vJoyInterfaceWrap;
using UITimer = System.Windows.Forms.Timer;
using System.Threading;

namespace XInputDemo
{
    /// <summary>
    /// Summary description for MainForm.
    /// </summary>
    public class MainForm : System.Windows.Forms.Form
    {
        static public vJoy joystick;
        static public vJoy.JoystickState iReport;
        static public uint id = 1;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.PictureBox pictureBox2;
        private System.Windows.Forms.TextBox rightTrigger;
        private System.Windows.Forms.TextBox leftTrigger;
        private System.Windows.Forms.TextBox rightStick;
        private System.Windows.Forms.TrackBar leftMotor;
        private System.Windows.Forms.TrackBar rightMotor;
        private IContainer components;
        private UITimer timer;
        private Bitmap mark;
        private Bitmap markAxisR;
        private Bitmap markAxisL;
        private Bitmap markLB;
        private Bitmap markRB;
        private Bitmap markLT;
        private Bitmap markRT;
        private Bitmap markFRT;
        private Bitmap markFLT;
        private Bitmap markFRB;
        private Bitmap markFLB;
        private ControllerButtons lastButtonsPressed = ControllerButtons.None;
        private int leftX;
        private int leftY;
        private int rightX;
        private int rightY;
        private bool leftTriggerB;
        private TextBox leftStick;
        private PictureBox pictureBox3;
        private ContextMenuStrip contextMenuStrip1;
        private ToolStripMenuItem setBackgroundToolStripMenuItem;
        private ToolStripMenuItem visibilityToolStripMenuItem;
        private ToolStripMenuItem stackedToolStripMenuItem;
        private ToolStripMenuItem sideBySideToolStripMenuItem;
        private ToolStripMenuItem singleViewToolStripMenuItem;
        private ToolStripMenuItem iconsToolStripMenuItem;
        private ToolStripMenuItem basicGreenToolStripMenuItem;
        private ToolStripMenuItem basicBlueToolStripMenuItem;
        private ToolStripMenuItem basicRedToolStripMenuItem;
        private ToolStripMenuItem exitToolStripMenuItem;
        private ToolStripMenuItem toolStripMenuItem1;
        private ToolStripMenuItem controller1ToolStripMenuItem;
        private ToolStripMenuItem controller2ToolStripMenuItem;
        private ToolStripMenuItem controller3ToolStripMenuItem;
        private ToolStripMenuItem controller4ToolStripMenuItem;
        private bool rightTriggerB;
        private bool extendedView;
        private ToolStripMenuItem StackedInvertedToolStripMenuItem;
        private int controllerBox = 0;
        private ToolStripMenuItem customToolStripMenuItem;
        private string path;
        private Worker workerObject;
        private Thread workerThread;
        private bool LMouse_button_state = false;
        private bool RMouse_button_state = false;
        private bool YMouse_button_state = false;

        [DllImport("user32.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
        public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);
        [DllImport("user32.dll", EntryPoint = "keybd_event", CharSet = CharSet.Auto, ExactSpelling = true)]
        public static extern void keybd_event(byte vk, byte scan, int flags, int extrainfo);
        private const int MOUSEEVENTF_MOVE = 0x01;
        private const int MOUSEEVENTF_LEFTDOWN = 0x02;
        private const int MOUSEEVENTF_LEFTUP = 0x04;
        private const int MOUSEEVENTF_RIGHTDOWN = 0x08;
        private const int MOUSEEVENTF_RIGHTUP = 0x10;

        public MainForm()
        {
            // Create one joystick object and a position structure.
            joystick = new vJoy();
            iReport = new vJoy.JoystickState();

            // Get the driver attributes (Vendor ID, Product ID, Version Number)
            if (!joystick.vJoyEnabled())
            {
                Console.WriteLine("vJoy driver not enabled: Failed Getting vJoy attributes.\n");
                return;
            }
            else
                Console.WriteLine("Vendor: {0}\nProduct :{1}\nVersion Number:{2}\n", joystick.GetvJoyManufacturerString(), joystick.GetvJoyProductString(), joystick.GetvJoySerialNumberString());

            // Get the state of the requested device
            VjdStat status = joystick.GetVJDStatus(id);
            switch (status)
            {
                case VjdStat.VJD_STAT_OWN:
                    Console.WriteLine("vJoy Device {0} is already owned by this feeder\n", id);
                    break;
                case VjdStat.VJD_STAT_FREE:
                    Console.WriteLine("vJoy Device {0} is free\n", id);
                    break;
                case VjdStat.VJD_STAT_BUSY:
                    Console.WriteLine("vJoy Device {0} is already owned by another feeder\nCannot continue\n", id);
                    return;
                case VjdStat.VJD_STAT_MISS:
                    Console.WriteLine("vJoy Device {0} is not installed or disabled\nCannot continue\n", id);
                    return;
                default:
                    Console.WriteLine("vJoy Device {0} general error\nCannot continue\n", id);
                    return;
            };

            // Check which axes are supported
            bool AxisX = joystick.GetVJDAxisExist(id, HID_USAGES.HID_USAGE_X);
            bool AxisY = joystick.GetVJDAxisExist(id, HID_USAGES.HID_USAGE_Y);
            bool AxisZ = joystick.GetVJDAxisExist(id, HID_USAGES.HID_USAGE_Z);
            bool AxisRX = joystick.GetVJDAxisExist(id, HID_USAGES.HID_USAGE_RX);
            bool AxisRZ = joystick.GetVJDAxisExist(id, HID_USAGES.HID_USAGE_RZ);
            // Get the number of buttons and POV Hat switchessupported by this vJoy device
            int nButtons = joystick.GetVJDButtonNumber(id);
            int ContPovNumber = joystick.GetVJDContPovNumber(id);
            int DiscPovNumber = joystick.GetVJDDiscPovNumber(id);

            // Print results
            Console.WriteLine("\nvJoy Device {0} capabilities:\n", id);
            Console.WriteLine("Numner of buttons\t\t{0}\n", nButtons);
            Console.WriteLine("Numner of Continuous POVs\t{0}\n", ContPovNumber);
            Console.WriteLine("Numner of Descrete POVs\t\t{0}\n", DiscPovNumber);
            Console.WriteLine("Axis X\t\t{0}\n", AxisX ? "Yes" : "No");
            Console.WriteLine("Axis Y\t\t{0}\n", AxisX ? "Yes" : "No");
            Console.WriteLine("Axis Z\t\t{0}\n", AxisX ? "Yes" : "No");
            Console.WriteLine("Axis Rx\t\t{0}\n", AxisRX ? "Yes" : "No");
            Console.WriteLine("Axis Rz\t\t{0}\n", AxisRZ ? "Yes" : "No");

            // Test if DLL matches the driver
            UInt32 DllVer = 0, DrvVer = 0;
            bool match = joystick.DriverMatch(ref DllVer, ref DrvVer);
            if (match)
                Console.WriteLine("Version of Driver Matches DLL Version ({0:X})\n", DllVer);
            else
                Console.WriteLine("Version of Driver ({0:X}) does NOT match DLL Version ({1:X})\n", DrvVer, DllVer);


            // Acquire the target
            if ((status == VjdStat.VJD_STAT_OWN) || ((status == VjdStat.VJD_STAT_FREE) && (!joystick.AcquireVJD(id))))
            {
                Console.WriteLine("Failed to acquire vJoy device number {0}.\n", id);
                return;
            }
            else
                Console.WriteLine("Acquired: vJoy device number {0}.\n", id);

            //
            // Required for Windows Form Designer support
            //
            InitializeComponent();
            controllerBox = 0;
            extendedView = false;
            //pictureBox1.Image = new Bitmap(String.Concat(path,"\\images\\/images/xboxControllerFront.png"));
            path = absPath();

            //Background images
            pictureBox1.Image = new Bitmap(this.GetType(), "xboxControllerFront.png");
            pictureBox2.Image = new Bitmap(this.GetType(), "xboxControllerTop.png");

            //Marks
            mark = new Bitmap(this.GetType(), "green_mark.png");
            markAxisL = new Bitmap(this.GetType(), "markAxis.png");
            markAxisR = new Bitmap(this.GetType(), "markAxis.png");
            markLB = new Bitmap(this.GetType(), "green_LB.png");
            markRB = new Bitmap(this.GetType(), "green_RB.png");
            markLT = new Bitmap(this.GetType(), "green_LT.png");
            markRT = new Bitmap(this.GetType(), "green_RT.png");

            //Extended triggers and bumpers
            markFLB = new Bitmap(this.GetType(), "green_FLB.png");
            markFRB = new Bitmap(this.GetType(), "green_FRB.png");
            markFLT = new Bitmap(this.GetType(), "green_FLT.png");
            markFRT = new Bitmap(this.GetType(), "green_FRT.png");


            pictureBox1.Paint += new PaintEventHandler(pictureBox1_Paint);
            pictureBox2.Paint += new PaintEventHandler(pictureBox2_Paint);

            timer = new UITimer();
            timer.Interval = 10;
            timer.Tick += new EventHandler(timer_Tick);
            timer.Start();

            // Create the thread object. This does not start the thread.
            workerObject = new Worker();
            workerThread = new Thread(workerObject.DoWork);

            // Start the worker thread.
            //workerThread.Start();
        }

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                workerObject.RequestStop();
                if (components != null)
                {
                    components.Dispose();
                }
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code
        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.setBackgroundToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.controller1ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.controller2ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.controller3ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.controller4ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.visibilityToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.stackedToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.StackedInvertedToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.sideBySideToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.singleViewToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.iconsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.basicGreenToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.basicBlueToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.basicRedToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.customToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.pictureBox2 = new System.Windows.Forms.PictureBox();
            this.rightTrigger = new System.Windows.Forms.TextBox();
            this.leftTrigger = new System.Windows.Forms.TextBox();
            this.rightStick = new System.Windows.Forms.TextBox();
            this.leftMotor = new System.Windows.Forms.TrackBar();
            this.rightMotor = new System.Windows.Forms.TrackBar();
            this.leftStick = new System.Windows.Forms.TextBox();
            this.pictureBox3 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.contextMenuStrip1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.leftMotor)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.rightMotor)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox3)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.BackColor = System.Drawing.Color.Black;
            this.pictureBox1.ContextMenuStrip = this.contextMenuStrip1;
            this.pictureBox1.Location = new System.Drawing.Point(12, 15);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(256, 191);
            this.pictureBox1.TabIndex = 11;
            this.pictureBox1.TabStop = false;
            this.pictureBox1.Click += new System.EventHandler(this.pictureBox1_Click);
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.setBackgroundToolStripMenuItem,
            this.toolStripMenuItem1,
            this.visibilityToolStripMenuItem,
            this.iconsToolStripMenuItem,
            this.exitToolStripMenuItem});
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(158, 136);
            this.contextMenuStrip1.Opening += new System.ComponentModel.CancelEventHandler(this.contextMenuStrip1_Opening);
            // 
            // setBackgroundToolStripMenuItem
            // 
            this.setBackgroundToolStripMenuItem.Name = "setBackgroundToolStripMenuItem";
            this.setBackgroundToolStripMenuItem.Size = new System.Drawing.Size(157, 22);
            this.setBackgroundToolStripMenuItem.Text = "Set Background";
            this.setBackgroundToolStripMenuItem.Click += new System.EventHandler(this.setBackgroundToolStripMenuItem_Click);
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.controller1ToolStripMenuItem,
            this.controller2ToolStripMenuItem,
            this.controller3ToolStripMenuItem,
            this.controller4ToolStripMenuItem});
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(157, 22);
            this.toolStripMenuItem1.Text = "Controller";
            // 
            // controller1ToolStripMenuItem
            // 
            this.controller1ToolStripMenuItem.Checked = true;
            this.controller1ToolStripMenuItem.CheckOnClick = true;
            this.controller1ToolStripMenuItem.CheckState = System.Windows.Forms.CheckState.Checked;
            this.controller1ToolStripMenuItem.Name = "controller1ToolStripMenuItem";
            this.controller1ToolStripMenuItem.Size = new System.Drawing.Size(136, 22);
            this.controller1ToolStripMenuItem.Text = "Controller 1";
            this.controller1ToolStripMenuItem.Click += new System.EventHandler(this.controller1ToolStripMenuItem_Click);
            // 
            // controller2ToolStripMenuItem
            // 
            this.controller2ToolStripMenuItem.CheckOnClick = true;
            this.controller2ToolStripMenuItem.Name = "controller2ToolStripMenuItem";
            this.controller2ToolStripMenuItem.Size = new System.Drawing.Size(136, 22);
            this.controller2ToolStripMenuItem.Text = "Controller 2";
            this.controller2ToolStripMenuItem.Click += new System.EventHandler(this.controller2ToolStripMenuItem_Click);
            // 
            // controller3ToolStripMenuItem
            // 
            this.controller3ToolStripMenuItem.CheckOnClick = true;
            this.controller3ToolStripMenuItem.Name = "controller3ToolStripMenuItem";
            this.controller3ToolStripMenuItem.Size = new System.Drawing.Size(136, 22);
            this.controller3ToolStripMenuItem.Text = "Controller 3";
            // 
            // controller4ToolStripMenuItem
            // 
            this.controller4ToolStripMenuItem.CheckOnClick = true;
            this.controller4ToolStripMenuItem.Name = "controller4ToolStripMenuItem";
            this.controller4ToolStripMenuItem.Size = new System.Drawing.Size(136, 22);
            this.controller4ToolStripMenuItem.Text = "Controller 4";
            this.controller4ToolStripMenuItem.Click += new System.EventHandler(this.controller4ToolStripMenuItem_Click);
            // 
            // visibilityToolStripMenuItem
            // 
            this.visibilityToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.stackedToolStripMenuItem,
            this.StackedInvertedToolStripMenuItem,
            this.sideBySideToolStripMenuItem,
            this.singleViewToolStripMenuItem});
            this.visibilityToolStripMenuItem.Name = "visibilityToolStripMenuItem";
            this.visibilityToolStripMenuItem.Size = new System.Drawing.Size(157, 22);
            this.visibilityToolStripMenuItem.Text = "Visibility";
            // 
            // stackedToolStripMenuItem
            // 
            this.stackedToolStripMenuItem.Checked = true;
            this.stackedToolStripMenuItem.CheckOnClick = true;
            this.stackedToolStripMenuItem.CheckState = System.Windows.Forms.CheckState.Checked;
            this.stackedToolStripMenuItem.Name = "stackedToolStripMenuItem";
            this.stackedToolStripMenuItem.Size = new System.Drawing.Size(169, 22);
            this.stackedToolStripMenuItem.Text = "Stacked";
            this.stackedToolStripMenuItem.Click += new System.EventHandler(this.stackedToolStripMenuItem_Click);
            // 
            // StackedInvertedToolStripMenuItem
            // 
            this.StackedInvertedToolStripMenuItem.CheckOnClick = true;
            this.StackedInvertedToolStripMenuItem.Name = "StackedInvertedToolStripMenuItem";
            this.StackedInvertedToolStripMenuItem.Size = new System.Drawing.Size(169, 22);
            this.StackedInvertedToolStripMenuItem.Text = "Stacked (inverted)";
            this.StackedInvertedToolStripMenuItem.Click += new System.EventHandler(this.StackedInvertedToolStripMenuItem_Click);
            // 
            // sideBySideToolStripMenuItem
            // 
            this.sideBySideToolStripMenuItem.CheckOnClick = true;
            this.sideBySideToolStripMenuItem.Name = "sideBySideToolStripMenuItem";
            this.sideBySideToolStripMenuItem.Size = new System.Drawing.Size(169, 22);
            this.sideBySideToolStripMenuItem.Text = "Side by side";
            this.sideBySideToolStripMenuItem.Click += new System.EventHandler(this.sideBySideToolStripMenuItem_Click);
            // 
            // singleViewToolStripMenuItem
            // 
            this.singleViewToolStripMenuItem.CheckOnClick = true;
            this.singleViewToolStripMenuItem.Name = "singleViewToolStripMenuItem";
            this.singleViewToolStripMenuItem.Size = new System.Drawing.Size(169, 22);
            this.singleViewToolStripMenuItem.Text = "Single view";
            this.singleViewToolStripMenuItem.Click += new System.EventHandler(this.singleViewToolStripMenuItem_Click);
            // 
            // iconsToolStripMenuItem
            // 
            this.iconsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.basicGreenToolStripMenuItem,
            this.basicBlueToolStripMenuItem,
            this.basicRedToolStripMenuItem,
            this.customToolStripMenuItem});
            this.iconsToolStripMenuItem.Name = "iconsToolStripMenuItem";
            this.iconsToolStripMenuItem.Size = new System.Drawing.Size(157, 22);
            this.iconsToolStripMenuItem.Text = "Icons";
            // 
            // basicGreenToolStripMenuItem
            // 
            this.basicGreenToolStripMenuItem.CheckOnClick = true;
            this.basicGreenToolStripMenuItem.Name = "basicGreenToolStripMenuItem";
            this.basicGreenToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.basicGreenToolStripMenuItem.Text = "Simple Green";
            this.basicGreenToolStripMenuItem.Click += new System.EventHandler(this.basicGreenToolStripMenuItem_Click);
            // 
            // basicBlueToolStripMenuItem
            // 
            this.basicBlueToolStripMenuItem.CheckOnClick = true;
            this.basicBlueToolStripMenuItem.Name = "basicBlueToolStripMenuItem";
            this.basicBlueToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.basicBlueToolStripMenuItem.Text = "Simple Blue";
            this.basicBlueToolStripMenuItem.Click += new System.EventHandler(this.basicBlueToolStripMenuItem_Click);
            // 
            // basicRedToolStripMenuItem
            // 
            this.basicRedToolStripMenuItem.CheckOnClick = true;
            this.basicRedToolStripMenuItem.Name = "basicRedToolStripMenuItem";
            this.basicRedToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.basicRedToolStripMenuItem.Text = "Simple Red";
            this.basicRedToolStripMenuItem.Click += new System.EventHandler(this.basicRedToolStripMenuItem_Click);
            // 
            // customToolStripMenuItem
            // 
            this.customToolStripMenuItem.CheckOnClick = true;
            this.customToolStripMenuItem.Name = "customToolStripMenuItem";
            this.customToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.customToolStripMenuItem.Text = "Custom";
            this.customToolStripMenuItem.Click += new System.EventHandler(this.customToolStripMenuItem_Click);
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(157, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // pictureBox2
            // 
            this.pictureBox2.BackColor = System.Drawing.Color.Black;
            this.pictureBox2.ContextMenuStrip = this.contextMenuStrip1;
            this.pictureBox2.Location = new System.Drawing.Point(12, 212);
            this.pictureBox2.Name = "pictureBox2";
            this.pictureBox2.Size = new System.Drawing.Size(256, 105);
            this.pictureBox2.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox2.TabIndex = 1;
            this.pictureBox2.TabStop = false;
            // 
            // rightTrigger
            // 
            this.rightTrigger.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.rightTrigger.Font = new System.Drawing.Font("Microsoft Sans Serif", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.rightTrigger.Location = new System.Drawing.Point(222, 557);
            this.rightTrigger.Name = "rightTrigger";
            this.rightTrigger.Size = new System.Drawing.Size(32, 18);
            this.rightTrigger.TabIndex = 2;
            this.rightTrigger.TabStop = false;
            this.rightTrigger.Text = "0";
            this.rightTrigger.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // leftTrigger
            // 
            this.leftTrigger.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.leftTrigger.Font = new System.Drawing.Font("Microsoft Sans Serif", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.leftTrigger.Location = new System.Drawing.Point(184, 557);
            this.leftTrigger.Name = "leftTrigger";
            this.leftTrigger.Size = new System.Drawing.Size(32, 18);
            this.leftTrigger.TabIndex = 3;
            this.leftTrigger.TabStop = false;
            this.leftTrigger.Text = "0";
            this.leftTrigger.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // rightStick
            // 
            this.rightStick.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.rightStick.Font = new System.Drawing.Font("Microsoft Sans Serif", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.rightStick.Location = new System.Drawing.Point(100, 557);
            this.rightStick.Name = "rightStick";
            this.rightStick.Size = new System.Drawing.Size(65, 18);
            this.rightStick.TabIndex = 4;
            this.rightStick.TabStop = false;
            this.rightStick.Text = "0;0";
            this.rightStick.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // leftMotor
            // 
            this.leftMotor.LargeChange = 1000;
            this.leftMotor.Location = new System.Drawing.Point(12, 418);
            this.leftMotor.Maximum = 65000;
            this.leftMotor.Name = "leftMotor";
            this.leftMotor.Size = new System.Drawing.Size(120, 45);
            this.leftMotor.TabIndex = 6;
            this.leftMotor.TickStyle = System.Windows.Forms.TickStyle.None;
            this.leftMotor.Scroll += new System.EventHandler(this.leftMotor_Scroll);
            // 
            // rightMotor
            // 
            this.rightMotor.LargeChange = 1000;
            this.rightMotor.Location = new System.Drawing.Point(12, 367);
            this.rightMotor.Maximum = 65000;
            this.rightMotor.Name = "rightMotor";
            this.rightMotor.Size = new System.Drawing.Size(120, 45);
            this.rightMotor.TabIndex = 8;
            this.rightMotor.TickStyle = System.Windows.Forms.TickStyle.None;
            this.rightMotor.Scroll += new System.EventHandler(this.rightMotor_Scroll);
            // 
            // leftStick
            // 
            this.leftStick.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.leftStick.Font = new System.Drawing.Font("Microsoft Sans Serif", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.leftStick.Location = new System.Drawing.Point(17, 557);
            this.leftStick.Name = "leftStick";
            this.leftStick.Size = new System.Drawing.Size(65, 18);
            this.leftStick.TabIndex = 5;
            this.leftStick.TabStop = false;
            this.leftStick.Text = "0;0";
            this.leftStick.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // pictureBox3
            // 
            this.pictureBox3.BackColor = System.Drawing.Color.Black;
            this.pictureBox3.ContextMenuStrip = this.contextMenuStrip1;
            this.pictureBox3.Location = new System.Drawing.Point(-17, -5);
            this.pictureBox3.Name = "pictureBox3";
            this.pictureBox3.Size = new System.Drawing.Size(732, 474);
            this.pictureBox3.TabIndex = 12;
            this.pictureBox3.TabStop = false;
            // 
            // MainForm
            // 
            this.AutoScaleBaseSize = new System.Drawing.Size(5, 13);
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(282, 329);
            this.ContextMenuStrip = this.contextMenuStrip1;
            this.Controls.Add(this.rightMotor);
            this.Controls.Add(this.leftMotor);
            this.Controls.Add(this.leftStick);
            this.Controls.Add(this.rightStick);
            this.Controls.Add(this.leftTrigger);
            this.Controls.Add(this.rightTrigger);
            this.Controls.Add(this.pictureBox2);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.pictureBox3);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.Text = "Xinput View";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.contextMenuStrip1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.leftMotor)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.rightMotor)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox3)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }
        #endregion

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.Run(new MainForm());
        }

        private void leftMotor_Scroll(object sender, System.EventArgs e)
        {
            XInput.Controllers[controllerBox].LeftMotorSpeed = (ushort)leftMotor.Value;
        }

        private void rightMotor_Scroll(object sender, System.EventArgs e)
        {
            XInput.Controllers[controllerBox].RightMotorSpeed = (ushort)rightMotor.Value;
        }

        private void timer_Tick(object sender, EventArgs e)
        {
            int X, Y;
            leftTriggerB = XInput.Controllers[controllerBox].State.Gamepad.LeftTrigger > 100;
            joystick.SetAxis(XInput.Controllers[controllerBox].State.Gamepad.LeftTrigger * 128, id, HID_USAGES.HID_USAGE_SL0);
            rightTriggerB = XInput.Controllers[controllerBox].State.Gamepad.RightTrigger > 100;
            joystick.SetAxis(XInput.Controllers[controllerBox].State.Gamepad.RightTrigger * 128, id, HID_USAGES.HID_USAGE_SL1);

            leftX = XInput.Controllers[controllerBox].State.Gamepad.ThumbLeftX / (32767 / 11);
            joystick.SetAxis(XInput.Controllers[controllerBox].State.Gamepad.ThumbLeftX / 2 + 16384, id, HID_USAGES.HID_USAGE_X);
            leftY = XInput.Controllers[controllerBox].State.Gamepad.ThumbLeftY / (32767 / 11);
            joystick.SetAxis(XInput.Controllers[controllerBox].State.Gamepad.ThumbLeftY / 2 + 16384, id, HID_USAGES.HID_USAGE_Y);

            if (Math.Abs(leftX) > 1 || Math.Abs(leftY) > 1)
            {
                X = XInput.Controllers[controllerBox].State.Gamepad.ThumbLeftX / (32767 / 20);
                Y = 0 - XInput.Controllers[controllerBox].State.Gamepad.ThumbLeftY / (32767 / 20);
                string stuff = X.ToString();
                mouse_event(MOUSEEVENTF_MOVE, (uint)X, (uint)Y, 0, 0);
                //MessageBox.Show(stuff, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }

            rightX = XInput.Controllers[controllerBox].State.Gamepad.ThumbRightX / (32767 / 11);
            joystick.SetAxis(XInput.Controllers[controllerBox].State.Gamepad.ThumbRightX / 2 + 16384, id, HID_USAGES.HID_USAGE_RX);
            rightY = XInput.Controllers[controllerBox].State.Gamepad.ThumbRightY / (32767 / 11);
            joystick.SetAxis(XInput.Controllers[controllerBox].State.Gamepad.ThumbRightY / 2 + 16384, id, HID_USAGES.HID_USAGE_RY);
            rightStick.Text = rightX + ";" + rightY;

            ControllerButtons buttons = XInput.Controllers[controllerBox].State.Gamepad.Buttons;
            //************ A
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.A)) joystick.SetBtn(true, id, 1);
            else joystick.SetBtn(false, id, 1);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.A))
            {
                if (!LMouse_button_state)
                {
                    X = Cursor.Position.X;
                    Y = Cursor.Position.Y;
                    LMouse_button_state = true;
                    mouse_event(MOUSEEVENTF_LEFTDOWN, (uint)X, (uint)Y, 0, 0);
                }
                
                
            }
            else
            {
                if (LMouse_button_state)
                {
                    X = Cursor.Position.X;
                    Y = Cursor.Position.Y;
                    LMouse_button_state = false;
                    mouse_event(MOUSEEVENTF_LEFTUP, (uint)X, (uint)Y, 0, 0);
                }
            }

            //****************** B
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.B)) joystick.SetBtn(true, id, 2);
            else joystick.SetBtn(false, id, 2);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.B))
            {
                if (!RMouse_button_state)
                {
                    X = Cursor.Position.X;
                    Y = Cursor.Position.Y;
                    RMouse_button_state = true;
                    mouse_event(MOUSEEVENTF_RIGHTDOWN, (uint)X, (uint)Y, 0, 0);
                }


            }
            else
            {
                if (RMouse_button_state)
                {
                    X = Cursor.Position.X;
                    Y = Cursor.Position.Y;
                    RMouse_button_state = false;
                    mouse_event(MOUSEEVENTF_RIGHTUP, (uint)X, (uint)Y, 0, 0);
                }
            }

            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.X)) joystick.SetBtn(true, id, 3);
            else joystick.SetBtn(false, id, 3);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Y)) joystick.SetBtn(true, id, 4);
            else joystick.SetBtn(false, id, 4);

            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Y))
            {
                if (!YMouse_button_state)
                {
                    YMouse_button_state = true;
                    keybd_event(0x5B, 0, 0, 0);
                }


            }
            else
            {
                if (YMouse_button_state)
                {
                    YMouse_button_state = false;
                    keybd_event(0x5B, 0, 0, 0x02);
                }
            }

            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ShoulderLeft)) joystick.SetBtn(true, id, 5);
            else joystick.SetBtn(false, id, 5);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ShoulderRight)) joystick.SetBtn(true, id, 6);
            else joystick.SetBtn(false, id, 6);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Back)) joystick.SetBtn(true, id, 7);
            else joystick.SetBtn(false, id, 7);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Start)) joystick.SetBtn(true, id, 8);
            else joystick.SetBtn(false, id, 8);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ThumbLeft)) joystick.SetBtn(true, id, 9);
            else joystick.SetBtn(false, id, 9);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ThumbRight)) joystick.SetBtn(true, id, 10);
            else joystick.SetBtn(false, id, 10);
            int pov = -1;
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Up) && XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Right)) pov = 4500;
            else if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Right) && XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Down)) pov = 13500;
            else if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Down) && XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Left)) pov = 22500;
            else if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Left) && XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Up)) pov = 31500;
            else if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Up)) pov = 0;
            else if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Right)) pov = 9000;
            else if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Down)) pov = 18000;
            else if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Left)) pov = 27000;
            joystick.SetContPov(pov, id, 1);
                
            this.pictureBox1.Refresh();
            this.pictureBox2.Refresh();
            lastButtonsPressed = buttons;
        }

        private void pictureBox1_Paint(object sender, PaintEventArgs e)
        {
            //Center of image
            int xShift = (int)mark.Size.Width / 2;
            int yShift = (int)mark.Size.Height / 2;
            int xShiftAxisL = (int)markAxisL.Size.Width / 2;
            int yShiftAxisL = (int)markAxisL.Size.Height / 2;
            int xShiftAxisR = (int)markAxisR.Size.Width / 2;
            int yShiftAxisR = (int)markAxisR.Size.Height / 2;

            //Sticks
            e.Graphics.DrawImage(markAxisR, (float)(161 - xShiftAxisL + rightX), (float)(103 - yShiftAxisL - rightY));
            e.Graphics.DrawImage(markAxisL, (float)(60 - xShiftAxisR + leftX), (float)(61 - yShiftAxisR - leftY));

            //Extended triggers and shoulder buttons
            if (leftTriggerB && extendedView) e.Graphics.DrawImage(markFLT, 62 - xShift, 11 - yShift);
            if (rightTriggerB && extendedView) e.Graphics.DrawImage(markFRT, 189 - xShift, 11 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ShoulderLeft) && extendedView) e.Graphics.DrawImage(markFLB, 46 - xShift, 27 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ShoulderRight) && extendedView) e.Graphics.DrawImage(markFRB, 185 - xShift, 27 - yShift);

            //Pad
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Up)) e.Graphics.DrawImage(mark, 91 - xShift, 88 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Down)) e.Graphics.DrawImage(mark, 91 - xShift, 117 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Left)) e.Graphics.DrawImage(mark, 77 - xShift, 103 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Right)) e.Graphics.DrawImage(mark, 105 - xShift, 103 - yShift);

            //Buttons
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Y)) e.Graphics.DrawImage(mark, 196 - xShift, 45 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.X)) e.Graphics.DrawImage(mark, 178 - xShift, 63 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.B)) e.Graphics.DrawImage(mark, 215 - xShift, 63 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.A)) e.Graphics.DrawImage(mark, 196 - xShift, 81 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Start)) e.Graphics.DrawImage(mark, 152 - xShift, 63 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.Back)) e.Graphics.DrawImage(mark, 102 - xShift, 63 - yShift);

            //Thumbstick buttons
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ThumbLeft)) e.Graphics.DrawImage(mark, 60 - xShift, 61 - yShift);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ThumbRight)) e.Graphics.DrawImage(mark, 161 - xShift, 103 - yShift);

        }

        private void pictureBox2_Paint(object sender, PaintEventArgs e)
        {
            //Center of image
            int xShiftLB = (int)markLB.Size.Width / 2;
            int yShiftLB = (int)markLB.Size.Height / 2;
            int xShiftRB = (int)markRB.Size.Width / 2;
            int yShiftRB = (int)markRB.Size.Height / 2;
            int xShiftRT = (int)markRT.Size.Width / 2;
            int yShiftRT = (int)markRT.Size.Height / 2;
            int xShiftLT = (int)markLT.Size.Width / 2;
            int yShiftLT = (int)markLT.Size.Height / 2;

            //Shoulder buttons
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ShoulderLeft)) e.Graphics.DrawImage(markLB, 58 - xShiftRB, 67 - yShiftRB);
            if (XInput.Controllers[controllerBox].IsButtonPressed(ControllerButtons.ShoulderRight)) e.Graphics.DrawImage(markRB, 197 - xShiftLB, 67 - yShiftRB);

            //Triggers
            if (leftTriggerB) e.Graphics.DrawImage(markLT, 62 - xShiftRT, 38 - yShiftRT);
            if (rightTriggerB) e.Graphics.DrawImage(markRT, 192 - xShiftLT, 38 - yShiftLT);

        }

        private void controllerBox_SelectedIndexChanged(object sender, System.EventArgs e)
        {

            if (!XInput.Controllers[controllerBox].IsConnected)
            {
                MessageBox.Show(this, "The controller with the index you selected is not connected to the \n" +
                                       "system or may be otherwise unavailable. Setting any properties on \n" +
                                       "this controller will fail silently and any state read from it will \n" +
                                       "contain the default values.", "Controller not connected", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void contextMenuStrip1_Opening(object sender, CancelEventArgs e)
        {

        }

        private void setBackgroundToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ColorDialog colorDlg = new ColorDialog();
            colorDlg.AllowFullOpen = true;
            colorDlg.AnyColor = true;
            colorDlg.SolidColorOnly = false;
            colorDlg.Color = Color.Red;

            if (colorDlg.ShowDialog() == DialogResult.OK)
            {
                pictureBox1.BackColor = colorDlg.Color;
                pictureBox2.BackColor = colorDlg.Color;
                pictureBox3.BackColor = colorDlg.Color;
            }
        }

        private void controller1ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            controllerBox = 0;
            controller1ToolStripMenuItem.Checked = true;
            controller2ToolStripMenuItem.Checked = false;
            controller3ToolStripMenuItem.Checked = false;
            controller4ToolStripMenuItem.Checked = false;
            if (!XInput.Controllers[controllerBox].IsConnected)
            {
                MessageBox.Show(this, "The controller with the index you selected is not connected to the \n" +
                                       "system or may be otherwise unavailable. Setting any properties on \n" +
                                       "this controller will fail silently and any state read from it will \n" +
                                       "contain the default values.", "Controller not connected", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void controller2ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            controllerBox = 1;
            controller1ToolStripMenuItem.Checked = false;
            controller2ToolStripMenuItem.Checked = true;
            controller3ToolStripMenuItem.Checked = false;
            controller4ToolStripMenuItem.Checked = false;
            if (!XInput.Controllers[controllerBox].IsConnected)
            {
                MessageBox.Show(this, "The controller with the index you selected is not connected to the \n" +
                                       "system or may be otherwise unavailable. Setting any properties on \n" +
                                       "this controller will fail silently and any state read from it will \n" +
                                       "contain the default values.", "Controller not connected", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void controller3ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            controllerBox = 2;
            controller1ToolStripMenuItem.Checked = false;
            controller2ToolStripMenuItem.Checked = false;
            controller3ToolStripMenuItem.Checked = true;
            controller4ToolStripMenuItem.Checked = false;
            if (!XInput.Controllers[controllerBox].IsConnected)
            {
                MessageBox.Show(this, "The controller with the index you selected is not connected to the \n" +
                                       "system or may be otherwise unavailable. Setting any properties on \n" +
                                       "this controller will fail silently and any state read from it will \n" +
                                       "contain the default values.", "Controller not connected", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void controller4ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            controllerBox = 3;
            controller1ToolStripMenuItem.Checked = false;
            controller2ToolStripMenuItem.Checked = false;
            controller3ToolStripMenuItem.Checked = false;
            controller4ToolStripMenuItem.Checked = true;
            if (!XInput.Controllers[controllerBox].IsConnected)
            {
                MessageBox.Show(this, "The controller with the index you selected is not connected to the \n" +
                                       "system or may be otherwise unavailable. Setting any properties on \n" +
                                       "this controller will fail silently and any state read from it will \n" +
                                       "contain the default values.", "Controller not connected", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }
        private void stackedToolStripMenuItem_Click(object sender, EventArgs e)
        {
            stackedToolStripMenuItem.Checked = true;
            StackedInvertedToolStripMenuItem.Checked = false;
            sideBySideToolStripMenuItem.Checked = false;
            singleViewToolStripMenuItem.Checked = false;
            extendedView = false;
            pictureBox1.Location = new Point(12, 15);
            pictureBox2.Location = new Point(12, 212);
            pictureBox2.Visible = true;
            MainForm.ActiveForm.Size = new System.Drawing.Size(288, 357);
        }

        private void StackedInvertedToolStripMenuItem_Click(object sender, EventArgs e)
        {
            stackedToolStripMenuItem.Checked = false;
            StackedInvertedToolStripMenuItem.Checked = true;
            sideBySideToolStripMenuItem.Checked = false;
            singleViewToolStripMenuItem.Checked = false;

            pictureBox2.Location = new Point(12, 15);
            pictureBox1.Location = new Point(12, 126);
            pictureBox2.Visible = true;
            MainForm.ActiveForm.Size = new System.Drawing.Size(288, 357);
        }

        private void sideBySideToolStripMenuItem_Click(object sender, EventArgs e)
        {
            stackedToolStripMenuItem.Checked = false;
            StackedInvertedToolStripMenuItem.Checked = false;
            sideBySideToolStripMenuItem.Checked = true;
            singleViewToolStripMenuItem.Checked = false;

            extendedView = false;
            pictureBox1.Location = new Point(12, 15);
            pictureBox2.Location = new Point(276, 44);
            pictureBox2.Visible = true;
            MainForm.ActiveForm.Size = new System.Drawing.Size(548, 243);
        }

        private void singleViewToolStripMenuItem_Click(object sender, EventArgs e)
        {
            stackedToolStripMenuItem.Checked = false;
            StackedInvertedToolStripMenuItem.Checked = false;
            sideBySideToolStripMenuItem.Checked = false;
            singleViewToolStripMenuItem.Checked = true;

            extendedView = true;
            pictureBox1.Location = new Point(12, 15);
            pictureBox2.Visible = false;
            MainForm.ActiveForm.Size = new System.Drawing.Size(288, 243);
        }

        private void basicGreenToolStripMenuItem_Click(object sender, EventArgs e)
        {
            basicGreenToolStripMenuItem.Checked = true;
            basicBlueToolStripMenuItem.Checked = false;
            basicRedToolStripMenuItem.Checked = false;
            customToolStripMenuItem.Checked = false;

            mark = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_mark.png"));
            markLB = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_LB.png"));
            markRB = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_RB.png"));
            markLT = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_LT.png"));
            markRT = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_RT.png"));
            markFLB = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_FLB.png"));
            markFRB = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_FRB.png"));
            markFLT = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_FLT.png"));
            markFRT = new Bitmap(String.Concat(path, "\\images\\green_icons\\green_FRT.png"));
        }

        private void basicBlueToolStripMenuItem_Click(object sender, EventArgs e)
        {
            basicGreenToolStripMenuItem.Checked = false;
            basicBlueToolStripMenuItem.Checked = true;
            basicRedToolStripMenuItem.Checked = false;
            customToolStripMenuItem.Checked = false;

            mark = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_mark.png"));
            markLB = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_LB.png"));
            markRB = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_RB.png"));
            markLT = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_LT.png"));
            markRT = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_RT.png"));
            markFLB = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_FLB.png"));
            markFRB = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_FRB.png"));
            markFLT = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_FLT.png"));
            markFRT = new Bitmap(String.Concat(path, "\\images\\blue_icons\\blue_FRT.png"));
        }
        private void basicRedToolStripMenuItem_Click(object sender, EventArgs e)
        {
            basicGreenToolStripMenuItem.Checked = false;
            basicBlueToolStripMenuItem.Checked = false;
            basicRedToolStripMenuItem.Checked = true;
            customToolStripMenuItem.Checked = false;

            mark = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_mark.png"));
            markLB = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_LB.png"));
            markRB = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_RB.png"));
            markLT = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_LT.png"));
            markRT = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_RT.png"));
            markFLB = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_FLB.png"));
            markFRB = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_FRB.png"));
            markFLT = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_FLT.png"));
            markFRT = new Bitmap(String.Concat(path, "\\images\\red_icons\\red_FRT.png"));
        }
        private void customToolStripMenuItem_Click(object sender, EventArgs e)
        {
            basicGreenToolStripMenuItem.Checked = false;
            basicBlueToolStripMenuItem.Checked = false;
            basicRedToolStripMenuItem.Checked = false;
            customToolStripMenuItem.Checked = true;

            mark = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_mark.png"));
            markLB = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_LB.png"));
            markRB = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_RB.png"));
            markLT = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_LT.png"));
            markRT = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_RT.png"));
            markFLB = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_FLB.png"));
            markFRB = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_FRB.png"));
            markFLT = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_FLT.png"));
            markFRT = new Bitmap(String.Concat(path, "\\images\\custom_icons\\custom_FRT.png"));
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Close();
        }

        private string absPath()
        {
            Assembly entryPoint = Assembly.GetEntryAssembly();
            string basePath = Path.GetDirectoryName(entryPoint.Location);
            return basePath;
        }


    }

    public class ReadOnlyComboBox : ComboBox
    {
        protected override void OnKeyDown(KeyEventArgs e)
        {
            e.Handled = true;
        }

        protected override void OnKeyPress(KeyPressEventArgs e)
        {
            e.Handled = true;
        }
    }

    public class Worker
    {
        // This method will be called when the thread is started. 
        public void DoWork()
        {
            //MessageBox.Show("Start", "Debug", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            var server = new NamedPipeServerStream("SpiffPipe", PipeDirection.InOut, 5);

            StreamReader reader = new StreamReader(server);
            server.WaitForConnection();
            //MessageBox.Show( "Listening", "Debug", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            while (!_shouldStop)
            {
                try
                {
                    if (server.IsConnected)
                    {
                        var line = reader.ReadLine();
                        if (line != null && line.Length > 0) 
                            MessageBox.Show(line, "Input", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    }
                    else
                    {
                        MessageBox.Show("Reconnecting pipe!", "Debug", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        server.WaitForConnection();
                    }

                }
                catch (IOException e)
                {
                    MessageBox.Show(e.Message, "ERROR", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }

            }
            //MessageBox.Show( "Stopped","Debug", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }
        public void RequestStop()
        {
            _shouldStop = true;
            //MessageBox.Show("Stopping", "Debug", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }
        // Volatile is used as hint to the compiler that this data 
        // member will be accessed by multiple threads. 
        private volatile bool _shouldStop;
    }
}
