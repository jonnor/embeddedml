
import machine
import gc
from drivers.ssd1306.ssd1306 import SSD1306_I2C as SSD

i2c_ext = machine.I2C("i2c1")

display_width = 128
display_height = 64
gc.collect()  # Precaution before instantiating framebuf

ssd = SSD(display_width, display_height, i2c_ext)
