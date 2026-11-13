import random
import time

from common import keyboard, led, uart, usb
from usb.device.keyboard import KeyCode

from cms import config, counter, direction, message_handler, times
from cms.jobs.bot import Bot


class Cleric(Bot):
    def __init__(self):
        super().__init__()

    def start(self):
        self.take_mp()
        self.feed_pet()
        self.use_skill(KeyCode.Q, 100_000, 5_000)
        self.use_skill(KeyCode.W, 200_000, 5_000)
        self.use_skill(KeyCode.E, 300_000, 5_000)
        self.attack(KeyCode.D, 800, 200)
        # self.move(10000, 1000)

    def move_left_then_right(self):
        """左右移动一下"""
        move_left_hold_ms = random.randint(100, 150)
        move_right_hold_ms = random.randint(100, 150)
        if self.is_face_right():
            # 向左移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, move_left_hold_ms)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, (300 - move_left_hold_ms))
            times.sleep_random_ms()
            self.change_direction()
        else:
            # 向右移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, move_right_hold_ms)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, (300 - move_right_hold_ms))
            times.sleep_random_ms()
            self.change_direction()
