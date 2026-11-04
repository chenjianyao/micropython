"""
组合 keyboard, mouse
usb.device.keyboard 和 usb.device.mouse 默认只能启用一个，也就是说设备只能做为键盘或者鼠标通讯
"""

import struct
import time

import machine
import usb.device
from micropython import const
from usb.device.hid import HIDInterface

_REPORT_ID_KEYBOARD = const(0x01)
_REPORT_ID_MOUSE = const(0x02)

_INTERFACE_PROTOCOL_KEYBOARD = const(0x01)

_KEY_ARRAY_LEN = const(6)  # Size of HID key array, must match report descriptor
_KEY_REPORT_LEN = const(_KEY_ARRAY_LEN + 2)  # Modifier Byte + Reserved Byte + Array entries

_INTERFACE_PROTOCOL_MOUSE = const(0x02)


class KeyboardMouseInterface(HIDInterface):
    """
    Synchronous USB keyboard HID interface
    A basic three button USB mouse HID interface
    """

    def __init__(self):
        super().__init__(
            _KEYBOARD_REPORT_DESC + _MOUSE_REPORT_DESC,
            set_report_buf=bytearray(1),
            interface_str="Composite Kbd/Mouse",
        )
        #
        # 键盘部分
        #
        self._key_reports = [
            bytearray(_KEY_REPORT_LEN),
            bytearray(_KEY_REPORT_LEN),
        ]  # Ping/pong report buffers
        self.numlock = False

        #
        # 鼠标部分
        #
        self._l = False  # Left button
        self._m = False  # Middle button
        self._r = False  # Right button
        self._buf = bytearray(3)

    #
    # 键盘部分
    #

    def on_set_report(self, report_data, _report_id, _report_type):
        self.on_led_update(report_data[0])

    def on_led_update(self, led_mask):
        # Override to handle keyboard LED updates. led_mask is bitwise ORed
        # together values as defined in LEDCode.
        pass

    def send_keys(self, down_keys, timeout_ms=100):
        # Update the state of the keyboard by sending a report with down_keys
        # set, where down_keys is an iterable (list or similar) of integer
        # values such as the values defined in KeyCode.
        #
        # Will block for up to timeout_ms if a previous report is still
        # pending to be sent to the host. Returns True on success.
        #
        # After passing a keycode value in down_keys, it's necessary to call the
        # function again without that key code set in order to release the key.
        #
        # Calling send_keys(()) (i.e. empty down_keys argument) will release all
        # keys.

        r, s = self._key_reports  # next report buffer to send, spare report buffer
        r[0] = 0  # modifier byte
        i = 2  # index for next key array item to write to
        for k in down_keys:
            if k < 0:  # Modifier key
                r[0] |= -k
            elif i < _KEY_REPORT_LEN:
                r[i] = k
                i += 1
            else:  # Excess rollover! Can't report
                r[0] = 0
                for i in range(2, _KEY_REPORT_LEN):
                    r[i] = 0xFF
                break

        while i < _KEY_REPORT_LEN:
            r[i] = 0
            i += 1

        # 在报告前加上 Report ID 后发送
        full_report = bytes([_REPORT_ID_KEYBOARD]) + bytes(r)
        if super().send_report(full_report, timeout_ms):
            # Swap buffers if the previous one is newly queued to send, so
            # any subsequent call can't modify that buffer mid-send
            self._key_reports[0] = s
            self._key_reports[1] = r
            return True
        return False

    #
    # 鼠标部分
    #

    def send_report(self, dx=0, dy=0):
        b = 0
        if self._l:
            b |= 1 << 0
        if self._r:
            b |= 1 << 1
        if self._m:
            b |= 1 << 2

        # Wait for any pending report to be sent to the host
        # before updating contents of _buf.
        #
        # This loop can be removed if you don't care about possibly missing a
        # transient report, the final report buffer contents will always be the
        # last one sent to the host (it just might lose one of the ones in the
        # middle).
        while self.busy():
            machine.idle()

        struct.pack_into("Bbb", self._buf, 0, b, dx, dy)

        full_report = bytes([_REPORT_ID_MOUSE]) + bytes(self._buf)
        return super().send_report(full_report)

    def click_left(self, down=True):
        self._l = down
        return self.send_report()

    def click_middle(self, down=True):
        self._m = down
        return self.send_report()

    def click_right(self, down=True):
        self._r = down
        return self.send_report()

    def move_by(self, dx, dy):
        if not -127 <= dx <= 127:
            raise ValueError("dx")
        if not -127 <= dy <= 127:
            raise ValueError("dy")
        return self.send_report(dx, dy)


# 键盘报告描述符 (添加了 Report ID 前缀 0x85, 0x01)
# HID keyboard report descriptor
#
# From p69 of http://www.usb.org/developers/devclass_docs/HID1_11.pdf
# fmt: off
_KEYBOARD_REPORT_DESC = (
    b'\x05\x01'     # Usage Page (Generic Desktop),
        b'\x09\x06'     # Usage (Keyboard),
    b'\xA1\x01'     # Collection (Application),
    b'\x85\x01'     # Report ID (1) -> 关键行
        b'\x05\x07'         # Usage Page (Key Codes);
            b'\x19\xE0'         # Usage Minimum (224),
            b'\x29\xE7'         # Usage Maximum (231),
            b'\x15\x00'         # Logical Minimum (0),
            b'\x25\x01'         # Logical Maximum (1),
            b'\x75\x01'         # Report Size (1),
            b'\x95\x08'         # Report Count (8),
            b'\x81\x02'         # Input (Data, Variable, Absolute), ;Modifier byte
            b'\x95\x01'         # Report Count (1),
            b'\x75\x08'         # Report Size (8),
            b'\x81\x01'         # Input (Constant), ;Reserved byte
            b'\x95\x05'         # Report Count (5),
            b'\x75\x01'         # Report Size (1),
        b'\x05\x08'         # Usage Page (Page# for LEDs),
            b'\x19\x01'         # Usage Minimum (1),
            b'\x29\x05'         # Usage Maximum (5),
            b'\x91\x02'         # Output (Data, Variable, Absolute), ;LED report
            b'\x95\x01'         # Report Count (1),
            b'\x75\x03'         # Report Size (3),
            b'\x91\x01'         # Output (Constant), ;LED report padding
            b'\x95\x06'         # Report Count (6),
            b'\x75\x08'         # Report Size (8),
            b'\x15\x00'         # Logical Minimum (0),
            b'\x25\x65'         # Logical Maximum(101),
        b'\x05\x07'         # Usage Page (Key Codes),
            b'\x19\x00'         # Usage Minimum (0),
            b'\x29\x65'         # Usage Maximum (101),
            b'\x81\x00'         # Input (Data, Array), ;Key arrays (6 bytes)
    b'\xC0'     # End Collection
)
# fmt: on

# 鼠标报告描述符 (添加了 Report ID 前缀 0x85, 0x02)
# Basic 3-button mouse HID Report Descriptor.
# This is based on Appendix E.10 of the HID v1.11 document.
# fmt: off
_MOUSE_REPORT_DESC = (
    b'\x05\x01'  # Usage Page (Generic Desktop)
        b'\x09\x02'  # Usage (Mouse)
    b'\xA1\x01'  # Collection (Application)
    b'\x85\x02'  # Report ID (2) -> 关键行
        b'\x09\x01'  # Usage (Pointer)
        b'\xA1\x00'  # Collection (Physical)
            b'\x05\x09'  # Usage Page (Buttons)
                b'\x19\x01'  # Usage Minimum (01),
                b'\x29\x03'  # Usage Maximum (03),
                b'\x15\x00'  # Logical Minimum (0),
                b'\x25\x01'  # Logical Maximum (1),
                b'\x95\x03'  # Report Count (3),
                b'\x75\x01'  # Report Size (1),
                b'\x81\x02'  # Input (Data, Variable, Absolute), ;3 button bits
                b'\x95\x01'  # Report Count (1),
                b'\x75\x05'  # Report Size (5),
                b'\x81\x01'  # Input (Constant), ;5 bit padding
            b'\x05\x01'  # Usage Page (Generic Desktop),
                b'\x09\x30'  # Usage (X),
                b'\x09\x31'  # Usage (Y),
                b'\x15\x81'  # Logical Minimum (-127),
                b'\x25\x7F'  # Logical Maximum (127),
                b'\x75\x08'  # Report Size (8),
                b'\x95\x02'  # Report Count (2),
                b'\x81\x06'  # Input (Data, Variable, Relative), ;2 position bytes (X & Y)
        b'\xC0'  # End Collection
    b'\xC0'  # End Collection
)
# fmt: on
