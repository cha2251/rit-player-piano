from queue import Queue
import pytest
from pynput import keyboard

from src.button_input.button_input import ButtonInput
from src.button_input.controller import ControllerButton
from src.communication.messages import Message, MessageType


class TestCreate:
    @pytest.mark.timeout(5)
    def test_create_button_input(self):
        testQueue = Queue()
        component = ButtonInput(testQueue)
        testDict = {'q': [53,54,55], 'w': [56], 'e': [57], 'r': [58], 't': [59], 'y': [60],
                ControllerButton.RightTrigger: [60],
                ControllerButton.Y: [61], 
                ControllerButton.LeftTrigger: [62],
                ControllerButton.X: [63],
                ControllerButton.LeftBumper: [64],
                ControllerButton.RightDPad: [65],
                ControllerButton.B: [66],
                ControllerButton.UpDPad: [67],
                ControllerButton.A: [68],
                ControllerButton.RightThumb: [69],
                ControllerButton.RightBumper: [70],
                ControllerButton.LeftThumb: [71]
                }
    
        expected = testDict
        actual = component.keyMap

        assert component.button_input_queue is testQueue
        assert expected == actual

        component.deactivate()

    def test_dict_preset(self):
        testQueue = Queue()
        testDict = {'q': 1, 'w': 2}
        component = ButtonInput(testQueue, testDict)

        expected = testDict
        actual = component.keyMap

        assert actual == expected

        component.deactivate()


class TestModify:
    @pytest.mark.timeout(1)
    def test_change_map(self):
        testQueue = Queue()
        component = ButtonInput(testQueue)
        testDict = {"c4":[ControllerButton.A], "d4":[ControllerButton.B], "e4":[ControllerButton.B]}

        expectedDict = {ControllerButton.A:[60], ControllerButton.B: [62,64]}

        testMessage = Message(MessageType.BUTTON_CONFIG_UPDATE, testDict)

        assert component.keyMap != testDict

        component.change_map(testMessage)

        actual = component.keyMap

        assert actual == expectedDict

        component.deactivate()


class TestRun:
    @pytest.mark.timeout(1)
    def test_exits(self):
        testQueue = Queue()
        component = ButtonInput(testQueue)

        component.deactivate()
