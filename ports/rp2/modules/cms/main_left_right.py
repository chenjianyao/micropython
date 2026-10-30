"""

先朝左 自动按 S
超过限制之后
反方向移动停下 再按 S

"""

import random
import time

from common import keyboard, led, times, usb
from usb.device.keyboard import KeyCode

from cms import counter, direction

# ========================================
max_z = 50

Q_PERIOD_MS = 100_000
E_PERIOD_MS = 200_000
T_PERIOD_MS = 300_000
JITTER_MS = 2_000  # 间隔抖动 ±2000ms

next_q_time = time.ticks_add(time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
next_e_time = time.ticks_add(time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
next_t_time = time.ticks_add(time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))

BASE_INTERVAL_MS = 800  # 基础间隔：每秒一次
INTERVAL_JITTER_MS = 300  # 间隔抖动 ±300ms

# ========================================
usb.init()
led.init()
keyboard.init()

# ========== 主循环 ==========
while True:
    now = time.ticks_ms()
    # ========== 1. led 闪烁 ==========
    led.blink()

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

        # 判断当前朝向，如果当前朝左，向右移动；如果当前朝右，则向左移动
        move_hold_ms1 = random.randint(80, 110)
        move_hold_ms2 = random.randint(80, 110)
        move_hold_ms3 = random.randint(80, 110)
        if direction.is_right():
            # 向左移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, move_hold_ms1)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, move_hold_ms2)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, move_hold_ms3)
            direction.set_face_left()
        else:
            # 向右移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, move_hold_ms3)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, move_hold_ms2)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, move_hold_ms1)
            direction.set_face_right()

    # ========== 增加干扰按键 ====================
    if counter.attack_count == max_z:
        max_z = random.randint(50, 65)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.Z)

    jitter = random.randint(-INTERVAL_JITTER_MS, INTERVAL_JITTER_MS)
    wait_ms = max(500, BASE_INTERVAL_MS + jitter)
    time.sleep_ms(wait_ms)
