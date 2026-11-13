"""
牧师
"""

import random
import time

from common import keyboard
from usb.device.keyboard import KeyCode

from cms import config, counter, direction, times

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
next_attack_time = time.ticks_ms()
next_turnaround_time = time.ticks_ms()
move_hold_ms = random.randint(3_000, 10_000)

BASE_INTERVAL_MS = 1000  # 基础间隔：每秒一次
INTERVAL_JITTER_MS = 300  # 间隔抖动 ±300ms

# 攻击键
ATTACK_KEY = KeyCode.D


def auto_play():
    # play_stand_still()
    play_keep_moving()


def play_stand_still():
    """牧师自动挂机，站桩不动"""
    global next_q_time
    global next_e_time
    global next_t_time
    global max_z
    now = time.ticks_ms()

    # ========== 1.自动按攻击键 [S] ====================
    keyboard.press_key(ATTACK_KEY)
    counter.increase_attack_count()

    # ========== 2.定时按辅助键 [Q, W, E, R, T] ==========
    if time.ticks_diff(now, next_q_time) >= 0:
        # 100 秒按一次 Q，W
        next_q_time = time.ticks_add(
            time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.Q)
        # counter.increase_skill_count()
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.W)
        # counter.increase_skill_count()

    elif time.ticks_diff(now, next_e_time) >= 0:
        # 200 秒按一次 E, R
        next_e_time = time.ticks_add(
            time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.E)
        counter.increase_skill_count()
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.R)
        # counter.increase_skill_count()

    elif time.ticks_diff(now, next_t_time) >= 0:
        # 300 秒按一次 T
        next_t_time = time.ticks_add(
            time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.T)
        counter.increase_skill_count()

    # =========== 3.自动左右移动 ===================
    # 攻击次数超限 100 下，左右运动
    # 技能次数超限 21 下，左右运动
    if counter.attack_count_exceeded_limit() or counter.skill_count_exceeded_limit():
        counter.init_attack_count()
        counter.init_skill_count()

        move_left_hold_ms = random.randint(100, 150)
        move_right_hold_ms = random.randint(100, 150)
        times.sleep_random_long_ms()

        # 判断当前朝向，如果当前朝左，向右移动；如果当前朝右，则向左移动
        if direction.is_right():
            # 向左移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, move_left_hold_ms)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.LEFT, (300 - move_left_hold_ms))
            direction.set_face_left()
        else:
            # 向右移动
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, move_right_hold_ms)
            times.sleep_random_ms()
            keyboard.press_key(KeyCode.RIGHT, (300 - move_right_hold_ms))
            direction.set_face_right()

    # ========== 4.增加干扰按键 ====================
    if counter.attack_count == max_z:
        max_z = random.randint(50, 65)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.Z)

    wait_ms = random.randint(500, 1000)
    time.sleep_ms(wait_ms)


def play_keep_moving():
    """牧师自动挂机，保持移动"""
    global next_q_time
    global next_e_time
    global next_t_time
    global max_z
    global next_attack_time
    global next_turnaround_time
    global move_hold_ms

    now = time.ticks_ms()
    # ========== 1.自动按攻击键 [S] ====================
    if time.ticks_diff(now, next_attack_time) >= 0:
        next_attack_time = time.ticks_add(time.ticks_ms(), random.randint(500, 1000))
        keyboard.press_key(ATTACK_KEY)

    # ========== 2.定时按辅助键 [Q, W, E, R, T] ==========
    if time.ticks_diff(now, next_q_time) >= 0:
        # 100 秒按一次 Q，W
        next_q_time = time.ticks_add(
            time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.Q)
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.W)

    elif time.ticks_diff(now, next_e_time) >= 0:
        # 200 秒按一次 E, R
        next_e_time = time.ticks_add(
            time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.E)
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.R)

    elif time.ticks_diff(now, next_t_time) >= 0:
        # 300 秒按一次 T
        next_t_time = time.ticks_add(
            time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS)
        )
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.T)

    # =========== 3.自动左右移动 ===================
    if time.ticks_diff(now, next_turnaround_time) >= 0:
        next_turnaround_time = time.ticks_add(time.ticks_ms(), move_hold_ms)
        # 判断当前朝向，如果当前朝左，向右移动；如果当前朝右，则向左移动
        if direction.is_right():
            keyboard.key_down(KeyCode.LEFT)
            direction.set_face_left()
        else:
            # 持续 3 到 10 秒
            move_hold_ms = random.randint(3_000, 10_000)
            keyboard.key_down(KeyCode.RIGHT)
            direction.set_face_right()

    # ========== 增加干扰按键 ====================
    if counter.attack_count == max_z:
        max_z = random.randint(50, 65)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.X)
