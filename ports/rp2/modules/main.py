"""

原地连续攻击 101 次，那么从第 102 次开始，攻击就会失效。横方向上移动半个身位，纵方向上移动大于 2 个身位
辅助技能同样生效，但阈值更低，通常原地使用 21 次后
宠物饥饿度大约每 30 秒下降 1 点，按照这个速度，饥饿度减少 30 点大约需要 900 秒，也就是 15 分钟。  

普通人
按键持续时间（keypress duration）约 80–150 毫秒，常见可粗略认为 100 毫秒左右
击键间隔（inter-key interval）普通打字者 200–300 ms；熟练者约 100–150 ms

"""
from machine import Pin
import machine
import time
import random
import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode
from cms import keyboard, led

# ========== 伪装参数 ==========  

current_attack_count = 0      # 攻击次数
max_attack = 80               # 最大攻击次数
max_z = 50

# 100 秒 Q，W
# 200 秒 E, R
# 300 秒 T
Q_PERIOD_MS   = 100_000
E_PERIOD_MS   = 200_000
T_PERIOD_MS   = 300_000
JITTER_MS     = 2_000      # 间隔抖动

next_q_time   = time.ticks_add(time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
next_e_time   = time.ticks_add(time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
next_t_time   = time.ticks_add(time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))

BOOT_DELAY_MS = 3000          # 上电后延迟 3 秒再开始
BASE_INTERVAL_MS = 800        # 基础间隔：每秒一次
INTERVAL_JITTER_MS = 300      # 间隔抖动 ±300ms


# 1. 启动延迟：在 USB 枚举完成后、开始发键之前等待
time.sleep_ms(BOOT_DELAY_MS)
led.init()
keyboard.init()

# ========== 主循环 ==========
while True:
    # ========== 1. led 闪烁 ==========
    led.blink()

    now = time.ticks_ms()
    # ========== 自动按攻击键 [S] ==================== 
    # 2. 自动按键
    keyboard.press_key(KeyCode.S)
    current_attack_count = current_attack_count + 1

    # ========== 定时按辅助键 [Q, W, E, R, T] ==========
    if time.ticks_diff(now, next_q_time) >= 0:
        # 100 秒按一次 Q，W
        next_q_time = time.ticks_add(time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.Q)
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.W)

    if time.ticks_diff(now, next_e_time) >= 0:
        # 200 秒按一次 E, R
        next_e_time = time.ticks_add(time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.E)
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.R)

    if time.ticks_diff(now, next_t_time) >= 0:
        # 300 秒按一次 T
        next_t_time = time.ticks_add(time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.T)

    # =========== 自动左右移动 =================== 
    # 攻击次数超限 100 下，左右运动
    if current_attack_count > max_attack:
        current_attack_count = 0
        max_attack = random.randint(65, 80)
        
        # 向左移动 X 毫秒
        move_hold_ms = random.randint(450, 550)
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.LEFT, move_hold_ms)

        # 跳一下
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.X)
        
        # 向右移动
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.RIGHT, move_hold_ms)

    # ========== 增加干扰按键 ====================
    if current_attack_count == max_z:
        max_z = random.randint(50, 65)
        keyboard.sleep_safe_ms()
        keyboard.press_key(KeyCode.Z)

    jitter = random.randint(-INTERVAL_JITTER_MS, INTERVAL_JITTER_MS)
    wait_ms = max(400, BASE_INTERVAL_MS + jitter)
    time.sleep_ms(wait_ms)
