import random
import time

from common import keyboard, led, usb
from usb.device.keyboard import KeyCode

from cms import counter, direction


def move_left(hold_ms):
    """朝左移动"""
    keyboard.press_key(KeyCode.LEFT, hold_ms)


def move_right(hold_ms):
    """朝右移动"""
    keyboard.press_key(KeyCode.LEFT, hold_ms)
