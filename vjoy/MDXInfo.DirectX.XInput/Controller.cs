using System;

namespace MDXInfo.DirectX.XInput
{
    public delegate void ControllerStateChangeEventHandler(Controller controller, State previousState, State currentState);
    public delegate void ControllerButtonEventHandler(Controller controller, ControllerButtons button);    

    /// <summary>
    /// Summary description for Controller.
    /// </summary>
    public class Controller
    {
        private static bool automaticallyPollState = true;

        /// <summary>
        /// May be used to turn automatic state polling on the controller on and off.
        /// If it's turned on (set to true, which is the default setting), each call 
        /// to access data on the controller object will polly the controller for the
        /// latest state. 
        /// 
        /// This may be redundant, so you can turn of this statis switch by setting it 
        /// to false. This means you will have to poll the controller state manually by
        /// calling the PollState() method. This could be done at the beginning of each
        /// frame for example, to prevent redundant polls to the controller
        /// 
        /// </summary>
        public static bool AutomaticallyPollState
        {
            get
            {
                return automaticallyPollState;
            }
            set
            {
                automaticallyPollState = value;
            }
        }

        // internal data structures to hold the data for a controller
        private int playerIndex = 0;

        public int PlayerIndex
        {
            get { return playerIndex; }
        }
        private State state = new State();
        private Vibration vibration = new Vibration();

        // only internal access to this class
        internal Controller(int playerIndex)
        {
            this.playerIndex = playerIndex;
        }

        /// <summary>
        /// Retrieves the current state of a controller by polling it using the XInput.GetState
        /// function. The result from this poll is stored in the internal State struct, which can
        /// be retrieved through this controller's State property.
        /// </summary>
        /// <returns>A boolean whether or not the poll was successful</returns>
        public bool PollState()
        {
            // this may be limited to once per frame or to a specific time period, using
            // AutomaticallyPollState to disable automatic polling through other accessors
            return XInput.GetState(this.playerIndex, ref this.state) == XInput.ERROR_SUCCESS;
        }

        private bool PollStateInternal()
        {
            if (AutomaticallyPollState)
            {
                return PollState();
            }
            else
            {
                return false;
            }
        }

        /// <summary>
        /// Checks whether data can be polled from the controller with the specified player index.
        /// If data cannot be polled, the controller typically is not connected.
        /// </summary>
        public bool IsConnected
        {
            get
            {
                return PollState();
            }
        }

        public ushort LeftMotorSpeed
        {
            get
            {
                return vibration.LeftMotorSpeed;
            }
            set
            {
                vibration.LeftMotorSpeed = value;
                XInput.SetState(this.playerIndex, ref this.vibration);
            }
        }

        public ushort RightMotorSpeed
        {
            get
            {
                return vibration.RightMotorSpeed;
            }
            set
            {
                vibration.RightMotorSpeed = value;
                XInput.SetState(this.playerIndex, ref this.vibration);
            }
        }

        public State State
        {
            get
            {
                PollStateInternal();
                return state;
            }
        }

        public bool IsButtonPressed(ControllerButtons buttonsToCheck)
        {
            PollStateInternal();
            return (this.state.Gamepad.Buttons & buttonsToCheck) != 0;
        }

        public void SetMotorSpeeds(ushort leftMotor, ushort rightMotor)
        {
            vibration.LeftMotorSpeed = leftMotor;
            vibration.RightMotorSpeed = rightMotor;
            XInput.SetState(this.playerIndex, ref this.vibration);
        }

        /// <summary>
        /// This region includes the methods and variable needed to 
        /// operate the event model for the controllers.
        /// </summary>
        #region Event model

        // Fired whenever a controller state changes
        public event ControllerStateChangeEventHandler StateChanged;

        // Utility events for quickly determining if button was pressed or released
        public event ControllerButtonEventHandler ButtonDown;
        public event ControllerButtonEventHandler ButtonUp;

        private State lastState;
        private bool firstEventPoll = true;

        /// <summary>
        /// Invoked by the static background thread in XInput to 
        /// poll state and fire events when needed.
        /// </summary>
        internal void PollForEvents()
        {
            if (PollState())
            {
                // make sure we have a lastState available
                if (!firstEventPoll)
                {
                    // make sure our new state isn't some delayed packet
                    if (state.PacketNumber > lastState.PacketNumber)
                    {
                        if (!state.Equals(lastState))
                        {
                            FireEvents(lastState, state);
                        }
                    }
                }

                lastState = this.state;
                firstEventPoll = false;
            }
        }

        private void FireEvents(State previous, State current)
        {
            if (StateChanged != null)
            {
                StateChanged(this, previous, current);
            }

            ControllerButtons[] buttons = (ControllerButtons[])Enum.GetValues(typeof(ControllerButtons));

            foreach (ControllerButtons button in buttons)
            {
                bool wasPressed = (previous.Gamepad.Buttons & button) != 0;
                bool isPressed = (current.Gamepad.Buttons & button) != 0;

                if (!wasPressed && isPressed)
                {
                    if (ButtonDown != null)
                    {
                        ButtonDown(this, button);
                    }
                }

                if (wasPressed & !isPressed)
                {
                    if (ButtonUp != null)
                    {
                        ButtonUp(this, button);
                    }
                }
            }
        }


        #endregion
    }
}
