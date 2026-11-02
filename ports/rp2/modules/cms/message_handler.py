"""消息处理器"""

from common import keyboard


def do_release():
    keyboard.key_up_all()


def do_keydown_key(key_name):
    """按下某个键并保持，直到收到对应的 keyup 或 release。"""
    key = _resolve(key_name)
    if key is None:
        return
    keyboard.key_down(key)


def do_keyup_key(key_name):
    """释放某个键。"""
    key = _resolve(key_name)
    if key is None:
        return
    keyboard.key_up(key)


def do_presskey_key(key_name, duration=None):
    key = _resolve(key_name)
    if key is None:
        return
    keyboard.press_key(key, duration)


def _resolve(key_name):
    """键名 -> KeyCode，未定义返回 None。"""
    return keyboard.KEY_MAP.get(key_name)
