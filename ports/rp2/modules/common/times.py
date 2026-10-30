import random
import time


def sleep_random_ms():
    """休眠 1000 - 1200ms"""
    hold_ms = random.randint(1000, 1200)

    time.sleep_ms(hold_ms)
