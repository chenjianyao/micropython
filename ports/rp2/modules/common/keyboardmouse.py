"""键盘与鼠标相关"""

import random
import time

import usb.device
from usb.device.keyboard import KeyCode
from usb.device.keyboardmouse import KeyboardMouseInterface

keyboardmouse = None
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
    """初始化键盘鼠标复合设备"""
    global keyboardmouse
    # 1. 创建键盘鼠标接口对象（准备“软件”）
    _keyboardmouse = KeyboardMouseInterface()
    # 2. 将接口注册到底层 USB 设备，并完成初始化（“点火”）builtin_driver 设为 False 禁用内置 USB 串口
    usb.device.get().init(_keyboardmouse, builtin_driver=False)

    # 3. 等待主机（电脑）完成枚举，确认连接就绪
    while not _keyboardmouse.is_open():
        time.sleep_ms(100)
    keyboardmouse = _keyboardmouse


def key_down(key):
    """按下按键"""
    if key not in pressed:
        pressed.add(key)
        keyboardmouse.send_keys(list(pressed))


def key_up(key):
    """释放按键，若为空列表，则表示全部释放"""
    if key in pressed:
        pressed.remove(key)
        keyboardmouse.send_keys(list(pressed))


def key_up_all():
    """释放所有按键"""
    pressed.clear()
    keyboardmouse.send_keys([])


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


def move_by(dx, dy):
    """人类运动的速度曲线近似钟形——启动时加速，中段较快，接近目标时减速。
    “末段减小步长”就是在模拟这种减速特性。WindMouse 的阻尼机制也是通过逐步降低步长来实现自然减速的。"""
    moved_x, moved_y = 0, 0
    while moved_x != dx or moved_y != dy:
        remaining_x = dx - moved_x
        remaining_y = dy - moved_y

        # 每一步的最大步长随机化，模拟速度波动
        # 靠近目标时步长自然减小（减速）
        base_step = random.randint(3, 15)
        if abs(remaining_x) + abs(remaining_y) < 100:
            base_step = random.randint(1, 5)  # 末段减速

        step_x = max(-base_step, min(base_step, remaining_x))
        step_y = max(-base_step, min(base_step, remaining_y))

        # 偶尔加入微小的反向或停顿，模拟手的“犹豫”
        if random.random() < 0.05:  # 5% 概率
            step_x += random.choice([-1, 0, 1])
            step_y += random.choice([-1, 0, 1])

        # 确保不超过 ±127 的硬件限制
        step_x = max(-127, min(127, step_x))
        step_y = max(-127, min(127, step_y))

        keyboardmouse.move_by(step_x, step_y)
        moved_x += step_x
        moved_y += step_y

        # 帧间延迟也随机化，模拟不匀速的节奏
        time.sleep_ms(random.randint(5, 20))


def _micro_jitter(steps=3):
    """在当前位置附近叠加微小抖动，模拟手部的自然震颤"""
    for _ in range(steps):
        # 抖动幅度 1~2 像素，方向随机
        jx = random.choice([-2, -1, 0, 0, 1, 2])
        jy = random.choice([-2, -1, 0, 0, 1, 2])
        keyboardmouse.move_by(jx, jy)
        time.sleep_ms(random.randint(10, 30))
    # 为了模拟“均值回归”，最后大致回拉（可选）


def click_left():
    keyboardmouse.click_left()


def click_right():
    keyboardmouse.click_right()
