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
 
# ========== 伪装参数 ==========  
led = None
kbd = None
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

def init_led():
    """ 初始化 led 灯"""
    global led
    # 板载 LED 接在 GP25
    
    _led = Pin(25, Pin.OUT)
    led = _led

def init_keyboard():
    """ 初始化键盘 """
    global kbd
    _kbd = KeyboardInterface()
    usb.device.get().init(_kbd, builtin_driver=True)

    # 等待主机打开键盘接口
    while not _kbd.is_open():
        time.sleep_ms(100)
    kbd = _kbd

def init_random_seed():
    seed = time.ticks_us()
    random.seed(seed)

def init():
    # 1. 启动延迟：在 USB 枚举完成后、开始发键之前等待
    time.sleep_ms(BOOT_DELAY_MS)
    init_led()
    init_keyboard()
    init_random_seed()

def blink():
    led.toggle()           # 翻转 LED 状态
    time.sleep_ms(100)     # 等待 0.5 秒

# ============================================================
# ========== 按键相关 ========================================= 
# ============================================================
pressed = set()                # 当前按下的键集合
KEYPRESS_DURATION_MIN_MS = 70  # 最短按住时长
KEYPRESS_DURATION_MAX_MS = 130 # 最长按住时长
KEYPRESS_INTERVAL_MIN_MS = 150 # 最短间隔时长
KEYPRESS_INTERVAL_MAX_MS = 250 # 最长间隔时长

def key_down(key):
    """ 按下按键 """
    if key not in pressed:
        pressed.add(key)
        kbd.send_keys(list(pressed))

def key_up(key):
    """ 释放按键，若为空列表，则表示全部释放 """
    if key in pressed:
        pressed.remove(key)
        kbd.send_keys(list(pressed))

def press_key(key, duration=None):
    """ 按键按下持续一段时间并释放 duration: 保持时长（秒），None 则随机"""
    if duration is None:
        hold_ms = random.randint(KEYPRESS_DURATION_MIN_MS, KEYPRESS_DURATION_MAX_MS)
    else:
        hold_ms = duration

    key_down(key)
    time.sleep_ms(hold_ms)
    key_up(key)

def press_key_interval(duration=None):
    """ 按键间隔 """
    if duration is None:
        hold_ms = random.randint(KEYPRESS_INTERVAL_MIN_MS, KEYPRESS_INTERVAL_MAX_MS)
    else:
        hold_ms = duration

    time.sleep_ms(hold_ms)

def sleep_safe_ms():
    hold_ms = random.randint(1000, 1200)

    time.sleep_ms(hold_ms)

# 初始化
init()

# ========== 主循环 ==========
while True:
    # ========== 1. led 闪烁 ==========
    blink()

    now = time.ticks_ms()
    # ========== 自动按攻击键 [S] ==================== 
    # 2. 自动按键
    press_key(KeyCode.S)
    current_attack_count = current_attack_count + 1

    # ========== 定时按辅助键 [Q, W, E, R, T] ==========
    if time.ticks_diff(now, next_q_time) >= 0:
        # 100 秒按一次 Q，W
        next_q_time = time.ticks_add(time.ticks_ms(), Q_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
        sleep_safe_ms()
        press_key(KeyCode.Q)
        sleep_safe_ms()
        press_key(KeyCode.W)

    if time.ticks_diff(now, next_e_time) >= 0:
        # 200 秒按一次 E, R
        next_e_time = time.ticks_add(time.ticks_ms(), E_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
        sleep_safe_ms()
        press_key(KeyCode.E)
        sleep_safe_ms()
        press_key(KeyCode.R)

    if time.ticks_diff(now, next_t_time) >= 0:
        # 300 秒按一次 T
        next_t_time = time.ticks_add(time.ticks_ms(), T_PERIOD_MS + random.randint(-JITTER_MS, JITTER_MS))
        sleep_safe_ms()
        press_key(KeyCode.T)

    # =========== 自动左右移动 =================== 
    # 攻击次数超限 100 下，左右运动
    if current_attack_count > max_attack:
        current_attack_count = 0
        max_attack = random.randint(65, 80)
        
        # 向左移动 X 毫秒
        move_hold_ms = random.randint(450, 550)
        sleep_safe_ms()
        press_key(KeyCode.LEFT, move_hold_ms)

        # 跳一下
        sleep_safe_ms()
        press_key(KeyCode.X)
        
        # 向右移动
        sleep_safe_ms()
        press_key(KeyCode.RIGHT, move_hold_ms)

    # ========== 增加干扰按键 ====================
    if current_attack_count == max_z:
        max_z = random.randint(50, 65)
        sleep_safe_ms()
        press_key(KeyCode.Z)

    jitter = random.randint(-INTERVAL_JITTER_MS, INTERVAL_JITTER_MS)
    wait_ms = max(400, BASE_INTERVAL_MS + jitter)
    time.sleep_ms(wait_ms)
 