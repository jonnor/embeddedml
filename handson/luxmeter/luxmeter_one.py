
import time
import machine
import array

import npyfile
import as7343
#from mini_encoder_c import MiniEncoderCHat

# I2C on Groove connector of M5StickC PLUS 2
i2c1 = machine.I2C(id=0, sda=32, scl=33)

# I2C on stick header, for stick Hat
i2c2 = machine.I2C(id=1, sda=0, scl=26)

def as7343_fifo_level(sensor) -> int:
    level = sensor.r_uint8(as7343.FIFO_LVL)
    return level


def measure_batch(sensor, filename, samples):
    
    n_channels = 18
    typecode = 'h' # int16
    shape = (n_channels, samples)

    with npyfile.Writer(filename, shape, typecode) as f:

        collected = 0
        while collected < samples:

            # check for new data
            level = as7343_fifo_level(sensor)
            if level >= 18:
                # TODO: use a pre-allocated array and read into that
                data = sensor.read_fifo()
                arr = array.array(typecode, data)
                f.write_values(arr)
                collected += 1
                yield collected

            # wait
            time.sleep_ms(10)


def foo():
    print('main-start')

    spectral = as7343.AS7343(i2c1)

    # Use FIFO
    spectral.start_measurement()
    spectral.set_integration_time(50*1000) # in us, max 182000 us
    spectral.set_measurement_time(200) # in ms

    spectral.set_illumination_current(60) # mA
    spectral.set_illumination_led(False)

    
    filename = 'data/one_4000k_868lux.npy'
    for s in measure_batch(spectral, filename, samples=20):
        print(s)

    print('Saved', filename)


print('run')
foo()

#if __name__ == '__main__':
#    main()

print('ran')

