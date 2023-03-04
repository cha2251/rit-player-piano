from queue import Queue
import pytest
from pynput import keyboard

from src.button_input.button_input import ButtonInput


class TestCreate:
    def test_create_button_input(self):
        testQueue = Queue()
        component = ButtonInput(testQueue)
        testDict = {'q': 55, 'w': 56, 'e': 57, 'r': 58, 't': 59,
                    'y': 60, 'u': 61, 'i': 62, 'o': 63, 'p': 64}

        expected = testDict
        actual = component.keyMap

        assert component.button_input_queue is testQueue
        assert expected == actual

    def test_dict_preset(self):
        testQueue = Queue()
        testDict = {'q': 1, 'w': 2}
        component = ButtonInput(testQueue, testDict)

        expected = testDict
        actual = component.keyMap

        assert actual == expected


class TestModify:
    def test_change_map(self):
        testQueue = Queue()
        component = ButtonInput(testQueue)
        testDict = {'q': 1, 'w': 2}

        assert component.keyMap != testDict

        component.change_map(testDict)

        expected = testDict
        actual = component.keyMap

        assert actual == expected


class TestRun:
    @pytest.mark.timeout(1)
    def test_exits(self):
        testQueue = Queue()
        component = ButtonInput(testQueue)

        component.run()

        component.deactivate()

    @pytest.mark.timeout(1)
    def test_detect_input(self):
        testQueue = Queue()
        component = ButtonInput(testQueue)

        component.run()
        component.on_press(keyboard.KeyCode.from_char('q'))
        component.on_release(keyboard.KeyCode.from_char('q'))
        component.deactivate()

        assert component.button_input_queue.empty() is False
