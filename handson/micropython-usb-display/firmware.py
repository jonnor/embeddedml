
# https://lilygo.cc/products/t3-s3-v1-3
# SDA--IO18; SCL--IO17

import ssd1306, ubinascii
from machine import Pin, I2C
#if 'oled' not in globals():

i2c = I2C(0, scl=Pin(17), sda=Pin(18))

print(i2c.scan())

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)                          # clear screen
oled.text("Hello, world!", 0, 0)      # x, y in pixels
oled.text("Line 2", 0, 10)
oled.rect(0, 20, 128, 30, 1)          # rectangle outline: x, y, w, h, color
oled.fill_rect(10, 25, 20, 20, 1)     # filled rectangle
oled.show()

