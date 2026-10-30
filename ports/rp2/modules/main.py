"""

原地连续攻击 101 次，那么从第 102 次开始，攻击就会失效。横方向上移动半个身位，纵方向上移动大于 2 个身位
辅助技能同样生效，但阈值更低，通常原地使用 21 次后
宠物饥饿度大约每 30 秒下降 1 点，按照这个速度，饥饿度减少 30 点大约需要 900 秒，也就是 15 分钟。

普通人
按键持续时间（keypress duration）约 80–150 毫秒，常见可粗略认为 100 毫秒左右
击键间隔（inter-key interval）普通打字者 200–300 ms；熟练者约 100–150 ms

"""

import random
import time

from cms import counter
from common import keyboard, led, times, usb
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

BASE_INTERVAL_MS = 1800  # 基础间隔：每秒一次
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

        # 向左移动
        move_hold_ms1 = random.randint(80, 90)
        move_hold_ms2 = random.randint(80, 90)
        move_hold_ms3 = random.randint(80, 90)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.LEFT, move_hold_ms1)
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.LEFT, move_hold_ms2)
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.LEFT, move_hold_ms3)

        # 攻击一下
        time.sleep_ms(10000)
        keyboard.press_key(KeyCode.S)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.S)

        # 向右移动
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.RIGHT, move_hold_ms3)
        # times.sleep_random_ms()
        # keyboard.press_key(KeyCode.RIGHT, move_hold_ms2)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.RIGHT, move_hold_ms1)

    # ========== 增加干扰按键 ====================
    if counter.attack_count == max_z:
        max_z = random.randint(50, 65)
        times.sleep_random_ms()
        keyboard.press_key(KeyCode.Z)

    jitter = random.randint(-INTERVAL_JITTER_MS, INTERVAL_JITTER_MS)
    wait_ms = max(500, BASE_INTERVAL_MS + jitter)
    time.sleep_ms(wait_ms)
