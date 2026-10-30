"""计数器"""

import random
import time

attack_count = 0  # 攻击次数
max_attack_count = random.randint(75, 85)  # 最大攻击次数


skill_count = 0  # 技能次数
max_skill_count = random.randint(15, 20)  # 最大技能次数


def init():
    init_attack_count()
    init_skill_count()


def init_attack_count():
    """攻击次数设置为 0"""
    global attack_count
    attack_count = 0
    global max_attack_count
    max_attack_count = random.randint(75, 85)


def increase_attack_count():
    """攻击次数 + 1"""
    global attack_count
    attack_count = attack_count + 1


def init_skill_count():
    """技能次数设置为 0"""
    global skill_count
    skill_count = 0
    global max_skill_count
    max_skill_count = random.randint(15, 20)


def increase_skill_count():
    """技能次数 + 1"""
    global skill_count
    skill_count = skill_count + 1


def attack_count_exceeded_limit():
    """攻击次数超限"""
    return attack_count >= max_attack_count


def skill_count_exceeded_limit():
    """技能次数超限"""
    return skill_count >= max_skill_count
