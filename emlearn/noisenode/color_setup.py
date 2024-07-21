
import gc
from machine import I2C, Pin

from drivers.ssd1306.ssd1306 import SSD1306_I2C as SSD

# LiLyGo T-Camera Mic
i2c = I2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
gc.collect()  # Precaution before instantiating framebuf
ssd = SSD(oled_width, oled_height, i2c)
