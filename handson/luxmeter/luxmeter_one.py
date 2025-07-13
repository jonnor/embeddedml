
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
    # FIXME: this should be the other way around!
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
                yield collected, arr

            # wait
            time.sleep_ms(10)


def foo():
    print('main-start')

    # Note: the measurement time is per set of 6 channels
    # So for 18 channels, effective time is 3x as long
    mtime = 100
    samples = 20
    filename = 'data/foo.npy'

    spectral = as7343.AS7343(i2c1)

    # Use FIFO
    spectral.start_measurement()
    spectral.set_integration_time(50*1000) # in us, max 182000 us
    spectral.set_measurement_time(mtime) # in ms

    spectral.set_illumination_current(60) # mA
    spectral.set_illumination_led(False)

    
    start = time.ticks_us()
    idx = spectral.CHANNEL_MAP.index('FZ')
    for s, data in measure_batch(spectral, filename, samples=samples):
        print('sample', time.ticks_ms(), s, data[idx])
    duration = time.ticks_diff(time.ticks_us(), start) / 1000
    print('recording-done', duration, duration/samples, mtime)

    print('Saved', filename)


print('run')
foo()

#if __name__ == '__main__':
#    main()

print('ran')

