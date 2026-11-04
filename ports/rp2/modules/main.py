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
from common import keyboard, led, uart, usb
from usb.device.keyboard import KeyCode

# ========================================
max_z = 50

# 100 秒 Q，W
# 200 秒 E, R
# 300 秒 T
Q_PERIOD_MS = 100_000
E_PERIOD_MS = 200_000
T_PERIOD_MS = 300_000
JITTER_MS = 2_000  # 间隔抖动

next_q_time = time.ticks_add(time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
next_e_time = time.ticks_add(time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
next_t_time = time.ticks_add(time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))

BASE_INTERVAL_MS = 1500  # 基础间隔：每秒一次
INTERVAL_JITTER_MS = 300  # 间隔抖动 ±300ms


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


def handle_single():
    global next_q_time
    global next_e_time
    global next_t_time
    global max_z
    now = time.ticks_ms()

    # ========== 2.自动按攻击键 [S] ====================
    keyboard.press_key(KeyCode.S)
    counter.increase_attack_count()

    # ========== 3.定时按辅助键 [Q, W, E, R, T] ==========
    if time.ticks_diff(now, next_q_time) >= 0:
        # 100 秒按一次 Q，W
        next_q_time = time.ticks_add(
            time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.Q)
        counter.increase_skill_count()
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.W)
        counter.increase_skill_count()

    elif time.ticks_diff(now, next_e_time) >= 0:
        # 200 秒按一次 E, R
        next_e_time = time.ticks_add(
            time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.E)
        counter.increase_skill_count()
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.R)
        counter.increase_skill_count()

    elif time.ticks_diff(now, next_t_time) >= 0:
        # 300 秒按一次 T
        next_t_time = time.ticks_add(
            time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.T)
        counter.increase_skill_count()

    # =========== 4.自动左右移动 ===================
    # 攻击次数超限 100 下，左右运动
    # 技能次数超限 21 下，左右运动
    if counter.attack_count_exceeded_limit() or counter.skill_count_exceeded_limit():
        counter.init_attack_count()
        counter.init_skill_count()

        move_hold_ms1 = random.randint(75, 85)
        # 判断当前朝向，如果当前朝左，向右移动；如果当前朝右，则向左移动

        if direction.is_right():
            # 向左移动 -> 向右移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, move_hold_ms1)
            time.sleep_ms(10000)
            keyboard.press_key(KeyCode.S)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, move_hold_ms1)
        else:
            # 向右移动 -> 向左移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, move_hold_ms1)
            time.sleep_ms(10000)
            keyboard.press_key(KeyCode.S)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, move_hold_ms1)

    # ========== 增加干扰按键 ====================
    if counter.attack_count == max_z:
        max_z = random.randint(50, 65)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.Z)

    jitter = random.randint(-INTERVAL_JITTER_MS, INTERVAL_JITTER_MS)
    wait_ms = max(500, BASE_INTERVAL_MS + jitter)
    time.sleep_ms(wait_ms)


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

# ========== 主循环 ==========
while True:
    now = time.ticks_ms()
    # ========== 1. led 闪烁 ==========
    led.blink()

    # ========== 2. 根据模式启动 ==========
    if config.mode == 1:
        handle_single()
    elif config.mode == 2:
        handle_pi()
    elif config.mode == 3:
        handle_single()
        handle_pi()
    else:
        handle_single()
        handle_pi()
