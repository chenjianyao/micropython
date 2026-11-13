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
        keyboard.press_key(KeyCode.F)
        self.take_mp()
        keyboard.press_key(KeyCode.G)
        self.feed_pet()
        keyboard.press_key(KeyCode.H)
        self.use_skill(KeyCode.Q, interval_ms=100_000, jitter_ms=5_000)
        self.use_skill(KeyCode.W, interval_ms=200_000, jitter_ms=5_000)
        self.use_skill(KeyCode.E, interval_ms=300_000, jitter_ms=5_000)
        self.attack(KeyCode.D, interval_ms=800, jitter_ms=200)
        keyboard.press_key(KeyCode.J)
        # self.move(interval_ms=10_000, jitter_ms=1_000)

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
