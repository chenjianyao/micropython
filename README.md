# MicroPython

MicroPython 可以理解为专门为微控制器（比如 RP2040 Pico）量身定制的、精简版的 Python 3。它让你能用熟悉的 Python 语法直接控制硬件，大大降低了嵌入式开发的门槛。

## 在 RP2040 Pico 上使用 MicroPython


## 冻结模块

将 Python 库（usb-device-keyboard, usb-device-mouse）在编译固件时就打包进去。

git clone --depth 1 --single-branch --branch v1.29.0 https://github.com/micropython/micropython-lib.git

手动将 lib/micropython-lib/micropyton/usb 目录下的文件拷贝到 ports/rp2/modules

## 编写运行代码

运行代码 ports/rp2/modules/main.py . Pico 上电后自动运行

## 烧录 MicroPython 固件

1. 进入 BOOTSEL 模式：按住 Pico 板上的 BOOTSEL 按钮不放，然后用 USB 线将它连接到电脑，连接后再松开按钮。
2. 拖拽烧录：此时电脑上会出现一个名为 RPI-RP2 的 U 盘。把下载好的 .uf2 文件拖拽到这个 U 盘里，Pico 会自动重启，MicroPython 就安装完成了。

