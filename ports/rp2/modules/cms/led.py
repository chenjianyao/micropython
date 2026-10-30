""" pico led 灯相关"""
from machine import Pin
import machine
import time
import random
import usb.device

led = None

def init():
    """ 初始化 led 灯 """
    global led
    # 板载 LED 接在 GP25
    
    _led = Pin(25, Pin.OUT)
    led = _led

def blink():
    """ led 灯闪烁 """
    led.toggle()           # 翻转 LED 状态
    time.sleep_ms(10)      # 等待 0.5 秒
