import machine
import time
from machine import Pin


def reg_read(i2c, addr, reg, nbytes=1):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """
    
    # Check to make sure caller is asking for 1 or more bytes
    if nbytes < 1:
        return bytearray()
    
    # Request data from specified register(s) over I2C
    print('READ', hex(addr), hex(reg), nbytes)
    data = i2c.readfrom_mem(addr, reg, nbytes)
    return data


I2C_ADDR = 0x71
REG_CHIPID = 0x30


# example code does this after i2c setup
time.sleep_ms(50*4)

def init():

    sda=Pin(17, Pin.OUT)
    scl=Pin(14, Pin.OUT)
    trig = scl

    # wakeup. Docs say to do this, but example code does not?
    # Pull SCL low for > 1 us, then high for >70 us
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(100)
    trig.value(0)
    time.sleep_ms(2)
    trig.value(1)
    
    # initialize I2C after using SCL as GPIO
    i2c = machine.I2C(1,
        scl=scl,
        sda=sda,
        freq=100000,
    )
    
    # Pull SCL low for at least 1 ms. Example code uses 20?
    #scl.value(0)
    #time.sleep_ms(20)
    #scl.value(1)
    #print("SCL")
    #scl.value(0)
    #time.sleep_ms(20)

    #acs = i2c.scan()
    #print("scan", [hex(a) for a in acs])

    chipid = reg_read(i2c, I2C_ADDR, REG_CHIPID, 2)
    print(list(hex(p) for p in chipid))

while True:
    try:
        init()
    except Exception as e:
        print(e)
    time.sleep(1)
