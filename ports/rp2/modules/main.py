""" """

import random
import time

from cms import counter, message_handler, times
from common import keyboard, led, uart, usb
from usb.device.keyboard import KeyCode

# ========================================

# ========================================
usb.init()
led.init()
keyboard.init()
uart.init()

# ========== 主循环 ==========
while True:
    now = time.ticks_ms()
    # ========== 1. led 闪烁 ==========
    led.blink()

    time.sleep_ms(500)
