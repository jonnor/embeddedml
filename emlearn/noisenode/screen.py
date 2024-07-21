
from machine import I2C, Pin

from machine import Pin, SoftI2C
import gc

import time
import random

import os
from machine import Pin
from machine import I2S

# Setups up the display
from color_setup import ssd

# On a monochrome display Writer is more efficient than CWriter.
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.meter import Meter
from gui.widgets.label import Label

# Fonts
import gui.fonts.courier20 as fixed
import gui.fonts.font6 as small


def render_display(db : float):
    start_time = time.ticks_ms()
    
    ssd.fill(0)
    #refresh(ssd)

    Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = Writer(ssd, fixed, verbose=False)
    wri.set_clip(False, False, False)

    warn_text = 'Loud!'
    numfield = Label(wri, 5, 0, wri.stringlen('99.9'))
    textfield = Label(wri, 40, 34, wri.stringlen(warn_text))

    numfield.value('{:5.1f} dBa'.format(db))

    if db > 75.0:
        textfield.value(warn_text, True)
    else:
        textfield.value('')

    refresh(ssd)

    duration = time.ticks_ms() - start_time
    print('render-display-done', duration)



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


AUDIO_BUFFER_LENGTH = 40000
AUDIO_BITDEPTH = 16
AUDIO_FORMAT = I2S.MONO
AUDIO_SAMPLERATE = 22050

SCK_PIN = 26
WS_PIN = 32
SD_PIN = 33

audio_in = I2S(0,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.RX,
    bits=AUDIO_BITDEPTH,
    format=AUDIO_FORMAT,
    rate=AUDIO_SAMPLERATE,
    ibuf=AUDIO_BUFFER_LENGTH,
)

# allocate sample arrays
chunk_samples = int(AUDIO_SAMPLERATE * 0.125)
mic_samples = bytearray(chunk_samples*AUDIO_BITDEPTH//2)
# memoryview used to reduce heap allocation in while loop
mic_samples_mv = memoryview(mic_samples)

soundlevel_db = 0.0

def audio_ready_callback(arg):
    global soundlevel_db

    print('audio-ready', time.ticks_ms())

    # TODO: compute soundlevel
    soundlevel_db = random.randint(35000, 95000) / 1000.0

    # re-trigger audio
    num_read = audio_in.readinto(mic_samples_mv)


def main():

    flip_display(ssd, vertical=False)

    # setting a callback function makes the readinto() method Non-Blocking
    audio_in.irq(audio_ready_callback)

    # Start microphoe readout. Callback will re-trigger it
    num_read = audio_in.readinto(mic_samples_mv)
    print('audio-start', num_read)

    while True:
        render_display(db=soundlevel_db)
        print('main-loop-iter', soundlevel_db)
        time.sleep_ms(100)

if __name__ == '__main__':
    main()


