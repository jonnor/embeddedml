
import time
import machine
import array

from aw9523 import AW9523
from as7343 import AS7343

i2c = machine.I2C("i2c1")
ext = AW9523(i2c, address=0x5b)
as7343 = AS7343(i2c)

as7343.set_measurement_time(200) # ms
as7343.set_integration_time(100*1000, repeat=1) # us
as7343.start_measurement()

while True:

    order = AS7343.CHANNEL_MAP

    print(order)
    # measure without exitation
    ext[0:16] = 0
    time.sleep(1.00)
    # XXX: make sure to flush out old readings from FIFO
    for i in range(20):
        readings = as7343.read()
    #as7343.stop_measurement()
    values = array.array('f', (readings[c] for c in order))
    print('off     ', readings['F7'], values)
    time.sleep(1.00)


    # Turn on exitation
    ext[0:16] = 100
    time.sleep(1.00)
    # XXX: make sure to flush out old readings from FIFO
    for i in range(20):
        readings = as7343.read()
    #as7343.stop_measurement()
    values = array.array('f', (readings[c] for c in order))
    print('excited!', readings['F7'], values)

    # TODO: turn on white LED, measure reflectance spectra


    time.sleep(5.0)
