import threading
from inputs import get_gamepad
from enum import Enum

class ControllerButton(Enum):
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
            'BTN_TL2': ControllerButton.LeftTrigger,
            'BTN_TR2': ControllerButton.RightTrigger,
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
        self.controller_listener = threading.Thread(target=self.listener, args=())
        self.controller_listener.daemon = True
        self.controller_listener.start()

    def listener(self):
        while self.active:
            events = get_gamepad()
            for event in events:
                # print(event.__dict__)

                if event.code in self.event_button_map:
                    self.on_controller_update(self.event_button_map[event.code], event.state)

    def deactivate(self):
        self.active = False
    