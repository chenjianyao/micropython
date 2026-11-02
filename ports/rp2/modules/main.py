""" """

import random
import time

from cms import counter, message_handler, times
from common import keyboard, led, uart, usb
from usb.device.keyboard import KeyCode


# ========================================
def handle_line(line):
    parts = line.split("_")
    if len(parts) < 2 or parts[0] != "PI":
        return

    cmd = parts[1]

    if cmd == "RELEASE":
        message_handler.do_release()
        return

    if len(parts) < 3 or not parts[2]:
        return
    key = parts[2]

    if cmd == "KEYDOWN":
        message_handler.do_keydown_key(key)

    elif cmd == "KEYUP":
        message_handler.do_keyup_key(key)

    elif cmd == "PRESSKEY":
        if len(parts) >= 4:
            try:
                duration = int(parts[3])
            except ValueError:
                return
            message_handler.do_presskey_key(key, duration)
        else:
            message_handler.do_presskey_key(key)

    else:
        return


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

    # 2) 非阻塞读一行串口
    line = uart.readline()
    if line:
        handle_line(line)

    time.sleep_ms(500)
