# main.py
# 接收树莓派 UART 指令，驱动 Pico 作为 USB HID 键盘
#
# 消息格式：
#   PI_KEYDOWN_A              按下 A 并保持
#   PI_KEYUP_A                释放 A
#   PI_PRESSKEY_A             按下 A 并释放（默认时长）
#   PI_PRESSKEY_A_3000        按下 A，3000ms 后释放
#   PI_RELEASE                释放所有按键
#   PI_CONFIG_B_BX            修改配置文件 config 中 B 的值
#

import random
import time

from cms import config, counter, direction, message_handler, times
from cms.jobs.cleric import Cleric
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

    elif cmd == "CONFIG":
        if len(parts) >= 4:
            config.setKeyValue(key, parts[3])
    else:
        return


def handle_pi():
    # 非阻塞读一行串口
    line = uart.readline()
    if line:
        handle_line(line)
    time.sleep_ms(5)


# ========================================
usb.init()
led.init()
keyboard.init()
uart.init()

cleric = Cleric()

# ========== 主循环 ==========
while True:
    now = time.ticks_ms()
    # ========== 1. led 闪烁 ==========
    led.blink()

    # ========== 2. 根据模式启动 ==========
    if config.mode == 1:
        cleric.start()
    elif config.mode == 2:
        handle_pi()
    elif config.mode == 3:
        cleric.start()
        handle_pi()
    else:
        cleric.start()
        handle_pi()
