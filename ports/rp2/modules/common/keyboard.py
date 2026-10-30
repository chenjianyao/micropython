"""键盘相关"""

import random
import time

import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode

kbd = None
# ============================================================
# ========== 按键相关 =========================================
# ============================================================
pressed = set()  # 当前按下的键集合
KEYPRESS_DURATION_MIN_MS = 70  # 最短按住时长
KEYPRESS_DURATION_MAX_MS = 130  # 最长按住时长
KEYPRESS_INTERVAL_MIN_MS = 150  # 最短间隔时长
KEYPRESS_INTERVAL_MAX_MS = 250  # 最长间隔时长


def init():
    """初始化键盘"""
    global kbd
    _kbd = KeyboardInterface()
    usb.device.get().init(_kbd, builtin_driver=True)

    # 等待主机打开键盘接口
    while not _kbd.is_open():
        time.sleep_ms(100)
    kbd = _kbd


def key_down(key):
    """按下按键"""
    if key not in pressed:
        pressed.add(key)
        kbd.send_keys(list(pressed))


def key_up(key):
    """释放按键，若为空列表，则表示全部释放"""
    if key in pressed:
        pressed.remove(key)
        kbd.send_keys(list(pressed))


def key_up_all():
    """释放所有按键"""
    pressed.clear()
    kbd.send_keys([])


def press_key(key, duration=None):
    """按键按下持续一段时间并释放 duration: 保持时长（秒），None 则随机"""
    if duration is None:
        hold_ms = random.randint(KEYPRESS_DURATION_MIN_MS, KEYPRESS_DURATION_MAX_MS)
    else:
        hold_ms = duration

    key_down(key)
    time.sleep_ms(hold_ms)
    key_up(key)


def press_key_interval(duration=None):
    """按键间隔"""
    if duration is None:
        hold_ms = random.randint(KEYPRESS_INTERVAL_MIN_MS, KEYPRESS_INTERVAL_MAX_MS)
    else:
        hold_ms = duration

    time.sleep_ms(hold_ms)
