

from buzzer_music import music

import time
import machine

success_song = """0 D5 2 43;2 E5 2 43;4 G5 4 43;8 C6 6 43;14 G5 2 43;16 E5 4 43;20 C5 4 43"""

#One buzzer on pin 0
buzzer_pin = machine.Pin(2)
mySong = music(success_song, pins=[buzzer_pin], looping=False)

#Four buzzers
#mySong = music(song, pins=[Pin(0),Pin(1),Pin(2),Pin(3)])

while True:
    running = mySong.tick()
    time.sleep_ms(30)
    #machine.lightsleep(40000)

