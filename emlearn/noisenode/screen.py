
from machine import I2C, Pin

from machine import Pin, SoftI2C
import gc

import time
import random

from color_setup import ssd
# On a monochrome display Writer is more efficient than CWriter.
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.meter import Meter
from gui.widgets.label import Label

# Fonts
import gui.fonts.courier20 as fixed
import gui.fonts.font6 as small


def fields():
    ssd.fill(0)
    refresh(ssd)
    Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = Writer(ssd, fixed, verbose=False)
    wri.set_clip(False, False, False)

    warn_text = 'Loud!'
    numfield = Label(wri, 5, 0, wri.stringlen('99.9'))
    textfield = Label(wri, 40, 34, wri.stringlen(warn_text))

    for s in range(0, 8):
        value = random.randint(40000, 80000) / 1000

        numfield.value('{:5.1f} dBa'.format(value))

        if value > 75.0:
            textfield.value(warn_text, True)
        else:
            textfield.value('')

        refresh(ssd)
        time.sleep(2)

    refresh(ssd)


def flip_display(ssd, vertical=False):
    """
    Vertical flip for SSD1306
    """

    SEGREMAP = 0xA0
    COMSCANINC = 0xc0
    COMSCANDEC = 0xc8

    if vertical:
        ssd.write_cmd(SEGREMAP | 0x01)
        ssd.write_cmd(COMSCANDEC)
    else:
        ssd.write_cmd(SEGREMAP)
        ssd.write_cmd(COMSCANINC)


flip_display(ssd, vertical=False)

print('Basic test of fields.')
fields()

