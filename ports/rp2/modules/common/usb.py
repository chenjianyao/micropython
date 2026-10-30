import time

BOOT_DELAY_MS = 3000          # 上电后延迟 3 秒再开始

def init():
    """ 启动延迟：在 USB 枚举完成后、开始发键之前等待 """
    # 1. 启动延迟：在 USB 枚举完成后、开始发键之前等待
    time.sleep_ms(BOOT_DELAY_MS)
