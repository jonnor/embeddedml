
import machine
from machine import SoftI2C, Pin
import time
import os
import array

import bma423
import axp202

#a.setChgLEDMode(axp202.AXP20X_LED_BLINK_1HZ)

# Enable LCD backlight
BACKLIGHT_LOW=2600
BACKLIGHT_MEDIUM=2950
BACKLIGHT_HIGH=3300
# XXX: Does not work? Might need to actually write something to the screen also
#a.enablePower(axp202.AXP202_LDO2)
#a.setLDO2Voltage(BACKLIGHT_HIGH) # 

def dir_exists(filename):
    try:
        return (os.stat(filename)[0] & 0x4000) != 0
    except OSError:
        return False

def log_state(i2c, time):

    # Enable tracking
    a = axp202.PMU(bus=i2c)
    a.enableADC(axp202.AXP202_ADC1, axp202.AXP202_VBUS_VOL_ADC1)
    a.enableADC(axp202.AXP202_ADC1, axp202.AXP202_VBUS_CUR_ADC1)
    a.enableADC(axp202.AXP202_ADC1, axp202.AXP202_BATT_VOL_ADC1)
    a.enableADC(axp202.AXP202_ADC1, axp202.AXP202_BATT_CUR_ADC1)

    voltage = a.getVbusVoltage()/1000.0
    percent = a.getBattPercentage()
    with open('battery-log.csv', 'a') as f:
        f.write('%s,%.2f,%d\n' % (time, voltage, percent))
    print("battery voltage=%.2f percent=%.1f%% " % (voltage, percent))

def isoformat(dt):
    # YEAR-MONTH-DAY T HOUR:MINUTE:SECOND
    # index nr 3 is weekday, ignored
    s = "%d-%02d-%02dT%02d:%02d:%02d" % (dt[0], dt[1], dt[2], dt[4], dt[5], dt[6])
    return s

def capture_acceleration(sensor, buffer, duration=10.0, samplerate=50):

    ms_sleep = int(1000/samplerate)
    samples = duration * samplerate

    if len(buffer) < samples*3:
        raise ValueError("Buffer is not large enough")

    samples_read = 0
    previous_time = None
    valid_sample = True
    while samples_read < samples:
        t = time.ticks_us()
        if previous_time is not None:
            delta_t = time.ticks_diff(t, previous_time)
            jitter = (delta_t/1000) - ms_sleep
            #print(jitter)
            if abs(jitter) > 3:
                #raise ValueError("Jitter too high")
                print("jitter too high", jitter)
                valid_sample = False
        
        # TODO: mark invalid sample
        x, y, z = sensor.get_xyz()
        idx = (samples_read * 3)
        buffer[idx+0] = x
        buffer[idx+1] = y
        buffer[idx+2] = z
        
        time.sleep_ms(ms_sleep)
        samples_read += 1
        previous_time = t


def write_buffer_csv(buffer, file):
    rowstride = 3
    rows = int(len(buffer) / rowstride)

    file.write('x,y,z\n')
    for row in range(0, rows):
        x = buffer[(row*rowstride)+0]
        y = buffer[(row*rowstride)+1]
        z = buffer[(row*rowstride)+2]
        fmt = '%.4f,%.4f,%.4f\n' % (x, y, z)
        file.write(fmt)

    file.flush()

rtc = machine.RTC() 
i2c = SoftI2C(scl=22,sda=21)

data_dir = 'data'
if not dir_exists(data_dir):
    os.mkdir(data_dir)


accel_samplerate = 50
accel_duration = 10.0
accel_samples = int(3 * accel_samplerate * accel_duration)
accel_buffer = array.array('f', ( 0 for _ in range(accel_samples)))

WAIT_SECONDS = 120.0-accel_duration

import st7789_ext

# https://github.com/Xinyuan-LilyGO/TTGO_TWatch_Library/blob/master/docs/watch_2020_v3.md
TFT_MOSI =19
TFT_SCLK =18
TFT_DC = 27
TFT_CS = 5
TFT_BACKLIGHT = 15

display_spi = SoftSPI(1, baudrate=40000000, phase=0, polarity=1,
    sck=TFT_SCLK,
    mosi=TFT_MOSI,
    miso=37
)

#vspi = SPI(2, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0,
#sck=Pin(18), mosi=Pin(23), miso=Pin(19))

display = st7789_ext.ST7789(
    display_spi,
    240, 240,
    reset=False,
    dc=machine.Pin(TFT_DC, machine.Pin.OUT),
    cs=machine.Pin(TFT_CS, machine.Pin.OUT),
)
display.init(landscape=False,mirror_y=True,mirror_x=True,inversion=True)

# NOTE: should be possible to PWM the backlight
backlight = machine.Pin(TFT_BACKLIGHT, machine.Pin.OUT)
backlight.set(1)

while True:
    dt = rtc.datetime()
    t = isoformat(dt)

    print('start-iter t='+ t)
    

    # TEMP
    continue


    log_state(i2c, t)
    sensor = bma423.BMA423(i2c, addr=0x19)
    
    path = data_dir + '/acceleration-'+t+'.csv'
    print('accel-capture-start')
    capture_acceleration(sensor, accel_buffer)
    print('accel-capture-end')
    with open(path, 'w') as f:
        write_buffer(accel_buffer, f)
    print('buffer-write-end')
    print('sleep-start')
    machine.lightsleep(int(1000*WAIT_SECONDS))
