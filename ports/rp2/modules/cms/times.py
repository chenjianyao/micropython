"""times"""

import random
import time


def sleep_random_ms():
    sleep_random_short_ms()


def sleep_random_short_ms():
    """休眠 200 - 500ms"""
    hold_ms = random.randint(200, 500)

    time.sleep_ms(hold_ms)


def sleep_random_long_ms():
    """休眠 1000 - 1200ms"""
    hold_ms = random.randint(1000, 1200)

    time.sleep_ms(hold_ms)
