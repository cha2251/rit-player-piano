import threading
from inputs import get_gamepad, UnpluggedError
from enum import IntEnum

class ControllerButton(IntEnum):
    LeftJoystickY = 1
    LeftJoystickX = 2
    RightJoystickY = 3
    RightJoystickX = 4
    LeftTrigger = 5
    RightTrigger = 6
    LeftBumper = 7
    RightBumper = 8
    A = 9
    X = 10
    Y = 11
    B = 12
    LeftThumb = 13
    RightThumb = 14
    Back = 15
    Start = 16
    LeftDPad = 17
    RightDPad = 18
    UpDPad = 19
    DownDPad = 20

class XboxController:
    def __init__(self, on_controller_update):
        # Map of event codes to controller buttons
        self.event_button_map = {
            'ABS_Y': ControllerButton.LeftJoystickY,
            'ABS_X': ControllerButton.LeftJoystickX,
            'ABS_RY': ControllerButton.RightJoystickY,
            'ABS_RX': ControllerButton.RightJoystickX,
            'ABS_Z': ControllerButton.LeftTrigger,
            'ABS_RZ': ControllerButton.RightTrigger,
            'BTN_TL': ControllerButton.LeftBumper,
            'BTN_TR': ControllerButton.RightBumper,
            'BTN_SOUTH': ControllerButton.A,
            'BTN_EAST': ControllerButton.B,
            'BTN_NORTH': ControllerButton.Y,
            'BTN_WEST': ControllerButton.X,
            'BTN_THUMBL': ControllerButton.LeftThumb,
            'BTN_THUMBR': ControllerButton.RightThumb,
            'BTN_SELECT': ControllerButton.Back,
            'BTN_START': ControllerButton.Start,
            'BTN_DPAD_LEFT': ControllerButton.LeftDPad,
            'BTN_DPAD_RIGHT': ControllerButton.RightDPad,
            'BTN_DPAD_UP': ControllerButton.UpDPad,
            'BTN_DPAD_DOWN': ControllerButton.DownDPad
        }

        self.on_controller_update = on_controller_update
        self.active = True

        # Weird buttons need state tracking to determine off events
        self.current_state = {'ABS_Z': 0, 'ABS_RZ': 0, 'BTN_DPAD_LEFT':0, 'BTN_DPAD_RIGHT':0, 'BTN_DPAD_UP':0, 'BTN_DPAD_DOWN':0}
        
        self.controller_listener = threading.Thread(target=self.listener, args=())
        self.controller_listener.daemon = True
        self.controller_listener.start()


    def listener(self):
        while self.active:
            try:
                events = get_gamepad()
            except UnpluggedError as e:
                print("No Gamepad Found")
                self.active = False
                break
            for event in events:
                try:
                    if self.clean_event(event):
                        self.on_controller_update(self.event_button_map[event.code], event.state)
                except KeyError as e:
                    pass # Expected if the event is not a mapped button press

    # Returns false if the event should be ignored
    def clean_event(self, event):
        # Maps triggers to 0 or 1 instead of analog values
        if event.code == 'ABS_Z' or event.code == 'ABS_RZ':
            if event.state == 0:
                self.current_state[event.code] = 0
                return True
            if self.current_state[event.code] == 0:
                self.current_state[event.code] = 1
                event.state = 1
                return True
            else:
                return False
        
        # Converts the DPad from two axis to four buttons
        if event.code == 'ABS_HAT0X':
            if event.state == 1:
                event.code = 'BTN_DPAD_RIGHT'
                self.current_state['BTN_DPAD_RIGHT'] = 1
            if event.state == -1:
                event.code = 'BTN_DPAD_LEFT'
                event.state = 1
                self.current_state['BTN_DPAD_LEFT'] = 1
            
            # Both DPad right and left off event are the same code, so have to check the state
            # If both are pressed, then this could fail, and turn off the right button even
            # though the left button was the one released. This is a known issue.
            if event.state == 0:
                if self.current_state['BTN_DPAD_LEFT'] == 1:
                    event.code = 'BTN_DPAD_LEFT'
                    self.current_state['BTN_DPAD_LEFT'] = 0
                    event.state = 0
                elif self.current_state['BTN_DPAD_RIGHT'] == 1:
                    event.code = 'BTN_DPAD_RIGHT'
                    self.current_state['BTN_DPAD_RIGHT'] = 0
                    event.state = 0
                else:
                    return False
                
        if event.code == 'ABS_HAT0Y':
            if event.state == 1:
                event.code = 'BTN_DPAD_DOWN'
                self.current_state['BTN_DPAD_DOWN'] = 1
            if event.state == -1:
                event.code = 'BTN_DPAD_UP'
                self.current_state['BTN_DPAD_UP'] = 1
                event.state = 1

            # Same as above, but for the DPad up and down
            if event.state == 0:
                if self.current_state['BTN_DPAD_UP'] == 1:
                    event.code = 'BTN_DPAD_UP'
                    self.current_state['BTN_DPAD_UP'] = 0
                    event.state = 0
                elif self.current_state['BTN_DPAD_DOWN'] == 1:
                    event.code = 'BTN_DPAD_DOWN'
                    self.current_state['BTN_DPAD_DOWN'] = 0
                    event.state = 0
                else:
                    return False

        return True


    def deactivate(self):
        self.active = False
    