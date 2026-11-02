"""
树莓派与 pico 通讯协议
树莓派使用 uart 与 pico 连接
树莓派发送指令。Pico 接收解析

"""

import random
import time

import machine

_uart = None
_buf = b""
_MAX_BUF = 512  # 防止长时间无换行时缓冲区无限增长


def init():
    """
    初始化 UART。

    重复调用会重新配置并清空内部缓冲。
    """
    global _uart, _buf
    # _uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))
    _uart = machine.UART(
        0,
        baudrate=9600,
        tx=machine.Pin(0),
        rx=machine.Pin(1),
        rxbuf=1024,  # 显式指定，避免 init 重置回默认 256
        timeout=0,  # 底层非阻塞
    )
    _buf = b""
    return _uart


def readline():
    """
    非阻塞读取一行。
    - 返回 str（已去掉行尾 \\r\\n 和首尾空白）
    - 没有完整行时返回 None
    - 空白行也被视为 None
    """
    global _buf
    if _uart is None:
        return None

    # 2) 非阻塞读取 UART
    # if _uart.any():
    #     chunk = _uart.read()
    #     if chunk:
    #         _buf += chunk
    #         while b"\n" in _buf:
    #             line, _buf = _buf.split(b"\n", 1)
    #             try:
    #                 text = line.decode("utf-8").strip()
    #             except Exception:
    #                 text = ""
    #             return text if text else None

    # 缓冲区里没有完整行时，尽量一次性取走当前所有可用字节
    if b"\n" not in _buf and _uart.any():
        data = _uart.read()
        if data:
            _buf += data

    # 仍无完整行
    if b"\n" not in _buf:
        if len(_buf) > _MAX_BUF:  # 超长且没有换行，丢弃防止内存膨胀
            _buf = b""
        return None

    # 切出第一行，剩余留在 _buf 供下次调用
    line, _buf = _buf.split(b"\n", 1)
    try:
        text = line.decode("utf-8").strip()
    except Exception:
        text = ""
    return text if text else None


def deinit():
    """
    释放 UART 资源。
    """
    global _uart, _buf
    if _uart is not None:
        try:
            _uart.deinit()
        except Exception:
            pass
    _uart = None
    _buf = b""
