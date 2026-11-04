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

KEY_MAP = {
    "A": KeyCode.A,
    "B": KeyCode.B,
    "C": KeyCode.C,
    "D": KeyCode.D,
    "E": KeyCode.E,
    "F": KeyCode.F,
    "G": KeyCode.G,
    "H": KeyCode.H,
    "I": KeyCode.I,
    "J": KeyCode.J,
    "K": KeyCode.K,
    "L": KeyCode.L,
    "M": KeyCode.M,
    "N": KeyCode.N,
    "O": KeyCode.O,
    "P": KeyCode.P,
    "Q": KeyCode.Q,
    "R": KeyCode.R,
    "S": KeyCode.S,
    "T": KeyCode.T,
    "U": KeyCode.U,
    "V": KeyCode.V,
    "W": KeyCode.W,
    "X": KeyCode.X,
    "Y": KeyCode.Y,
    "Z": KeyCode.Z,
    "N1": KeyCode.N1,
    "N2": KeyCode.N2,
    "N3": KeyCode.N3,
    "N4": KeyCode.N4,
    "N5": KeyCode.N5,
    "N6": KeyCode.N6,
    "N7": KeyCode.N7,
    "N8": KeyCode.N8,
    "N9": KeyCode.N9,
    "N0": KeyCode.N0,
    "F1": KeyCode.F1,
    "F2": KeyCode.F2,
    "F3": KeyCode.F3,
    "F4": KeyCode.F4,
    "F5": KeyCode.F5,
    "F6": KeyCode.F6,
    "F7": KeyCode.F7,
    "F8": KeyCode.F8,
    "F9": KeyCode.F9,
    "F10": KeyCode.F10,
    "F11": KeyCode.F11,
    "F12": KeyCode.F12,
    "ENTER": KeyCode.ENTER,
    "SPACE": KeyCode.SPACE,
    "TAB": KeyCode.TAB,
    "ESC": KeyCode.ESCAPE,
    "BACKSPACE": KeyCode.BACKSPACE,
    "PRINTSCREEN": KeyCode.PRINTSCREEN,
    "SCROLLLOCK": KeyCode.SCROLL_LOCK,
    "PAUSE": KeyCode.PAUSE,
    "INSERT": KeyCode.INSERT,
    "HOME": KeyCode.HOME,
    "PAGEUP": KeyCode.PAGEUP,
    "DELETE": KeyCode.DELETE,
    "END": KeyCode.END,
    "PAGEDOWN": KeyCode.PAGEDOWN,
    "RIGHT": KeyCode.RIGHT,
    "LEFT": KeyCode.LEFT,
    "DOWN": KeyCode.DOWN,
    "UP": KeyCode.UP,
    "CTRL": KeyCode.LEFT_CTRL,
    "SHIFT": KeyCode.LEFT_SHIFT,
    "ALT": KeyCode.LEFT_ALT,
}


def init():
    """初始化键盘"""
    global kbd
    # 1. 创建键盘接口对象（准备“软件”）
    _kbd = KeyboardInterface()
    # 2. 将接口注册到底层 USB 设备，并完成初始化（“点火”）builtin_driver 设为 False 禁用内置 USB 串口
    usb.device.get().init(_kbd, builtin_driver=False)

    # 3. 等待主机（电脑）完成枚举，确认连接就绪
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
