"""鼠标操作"""

import random
import time

import usb.device
from usb.device.mouse import MouseInterface

mouse = None


def init():
    """初始化鼠标"""
    global mouse
    # 1. 创建鼠标接口对象（准备“软件”）
    _mouse = MouseInterface()
    # 2. 将接口注册到底层 USB 设备，并完成初始化（“点火”）builtin_driver 设为 False 禁用内置 USB 串口
    usb.device.get().init(_mouse, builtin_driver=False)

    # 3. 等待主机（电脑）完成枚举，确认连接就绪
    while not _mouse.is_open():
        time.sleep_ms(100)

    mouse = _mouse


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

        mouse.move_by(step_x, step_y)
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
        mouse.move_by(jx, jy)
        time.sleep_ms(random.randint(10, 30))
    # 为了模拟“均值回归”，最后大致回拉（可选）


def click_left():
    mouse.click_left()


def click_right():
    mouse.click_right()
