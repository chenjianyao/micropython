import random
import time

from common import keyboard, led, uart, usb
from usb.device.keyboard import KeyCode

from cms import config, counter, direction, message_handler, times

LEFT = "left"
RIGHT = "right"

# 攻击键
ATTACK_KEY = KeyCode.D
# 跳跃键
JUMP_KEY = KeyCode.X
# 拾取键
PICKUP_KEY = KeyCode.Z

# 喂宠物键
FEED_PET_INTERVAL_MS = 600_000  # 10 分钟
FEED_PET_KEY = KeyCode.T

# 喂蓝键
TAKE_MP_INTERVAL_MS = 180_000  # 3 分钟
TAKE_MP_KEY = KeyCode.R


class Bot:
    def __init__(self):
        self._running = False
        self.attack_count = 0
        self.attack_count_limit = random.randint(80, 100)  # 最大攻击次数
        self.last_attack_time = None
        self.skill_count = 0
        self.skill_count_limit = random.randint(80, 100)  # 最大技能次数
        self.last_skill_time = None
        self.direction = RIGHT
        # key -> 下次可执行的时刻 (ticks_ms)
        # 用 key 区分不同技能/动作，避免互相干扰
        self._next_time = {
            str(FEED_PET_KEY): time.ticks_ms() + FEED_PET_INTERVAL_MS,
            str(TAKE_MP_KEY): time.ticks_ms() + TAKE_MP_INTERVAL_MS,
        }
        ############# MP  #############
        # self.next_take_mp_time = time.ticks_ms() + TAKE_MP_INTERVAL_MS
        ############# 宠物 #############
        # self.next_feed_pet_time = time.ticks_ms() + FEED_PET_INTERVAL_MS

    def start(self):
        """子类实现"""
        pass

    def _jittered(self, interval_ms, jitter_ms):
        """返回带抖动的实际间隔，保证 >= 0"""
        if jitter_ms <= 0:
            return interval_ms
        # 对称抖动：间隔在 [interval - jitter, interval + jitter] 之间随机
        actual = interval_ms + random.randint(-jitter_ms, jitter_ms)
        if actual > 0:
            return actual
        return 0

    def _ready(self, key, interval_ms, jitter_ms=0):
        """
        距离上次成功执行是否已经超过 interval_ms。
        返回 True 表示现在可以执行，并自动记录下次可执行时间。
        """
        now = time.ticks_ms()
        next_time = self._next_time.get(str(key), None)
        # 首次执行，或已到达/超过预定时刻
        if next_time is None or time.ticks_diff(now, next_time) >= 0:
            actual_interval = self._jittered(interval_ms, jitter_ms)
            self._next_time[str(key)] = time.ticks_add(now, actual_interval)
            return True

        return False

    def attack(self, key=ATTACK_KEY, interval_ms=800, jitter_ms=200):
        """攻击，间隔 ATTACK_INTERVAL_MS 毫秒，抖动 ATTACK_JITTER_MS 毫秒"""
        # 检查攻击次数是否超过限制
        if self.attack_count >= self.attack_count_limit:
            # 重置攻击次数和限制
            self.attack_count = 0
            self.attack_count_limit = random.randint(80, 100)
            # 左右移动一下
            self.move_left_then_right()

        if self._ready(key, interval_ms, jitter_ms):
            keyboard.press_key(ATTACK_KEY)
            self.attack_count = self.attack_count + 1
            self.last_attack_time = time.ticks_ms()

    def use_skill(self, key, interval_ms=0, jitter_ms=0):
        """使用技能，间隔 interval_ms 毫秒，抖动 jitter_ms 毫秒"""

        # 检查技能次数是否超过限制
        if self.skill_count >= self.skill_count_limit:
            # 重置技能次数和限制
            self.skill_count = 0
            self.skill_count_limit = random.randint(80, 100)
            # 左右移动一下
            self.move_left_then_right()

        if self._ready(key, interval_ms, jitter_ms):
            keyboard.press_key(key)
            self.skill_count = self.skill_count + 1
            self.last_skill_time = time.ticks_ms()

    def feed_pet(self, key=FEED_PET_KEY, interval_ms=FEED_PET_INTERVAL_MS, jitter_ms=5_000):
        """喂宠物 10min"""
        if self._ready(key, interval_ms, jitter_ms):
            keyboard.press_key(key)

        # if time.ticks_diff(time.ticks_ms(), self.next_feed_pet_time) >= 0:
        #     keyboard.press_key(FEED_PET_KEY)
        #     self.next_feed_pet_time = time.ticks_add(
        #         time.ticks_ms(), FEED_PET_INTERVAL_MS + random.randint(-5_000, 5_000)
        #     )

    def take_mp(self, key=TAKE_MP_KEY, interval_ms=TAKE_MP_INTERVAL_MS, jitter_ms=5_000):
        """吃蓝 3min"""
        if self._ready(key, interval_ms, jitter_ms):
            keyboard.press_key(key)

        # if time.ticks_diff(time.ticks_ms(), self.next_take_mp_time) >= 0:
        #     keyboard.press_key(TAKE_MP_KEY)
        #     self.next_take_mp_time = time.ticks_add(
        #         time.ticks_ms(), TAKE_MP_INTERVAL_MS + random.randint(-5_000, 5_000)
        #     )

    def move(self, interval_ms=1000, jitter_ms=0):
        """子类实现"""
        self.attack_count = 0
        self.skill_count = 0
        if self._ready(KeyCode.LEFT, interval_ms, jitter_ms):
            if self.is_face_right():
                # 向左移动
                keyboard.key_up_all()
                keyboard.key_down(KeyCode.LEFT)
                self.change_direction()
            else:
                # 向右移动
                keyboard.key_up_all()
                keyboard.key_down(KeyCode.RIGHT)
                self.change_direction()

    def move_left(self):
        """子类实现"""
        self.attack_count = 0
        self.skill_count = 0

    def move_right(self):
        """子类实现"""
        self.attack_count = 0
        self.skill_count = 0

    def move_left_then_right(self):
        """子类实现"""
        pass

    def jump(self):
        """子类实现"""
        keyboard.press_key(JUMP_KEY)

    def pickup(self):
        """子类实现"""
        keyboard.press_key(PICKUP_KEY)

    def is_face_left(self):
        return self.direction == LEFT

    def is_face_right(self):
        return self.direction == RIGHT

    def change_direction(self):
        """改变朝向"""
        if self.is_face_left():
            self.direction = RIGHT
        else:
            self.direction = LEFT
