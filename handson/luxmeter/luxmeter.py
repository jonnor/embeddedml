
import time
import machine

import as7343

# I2C on Groove connector of M5StickC PLUS 2
i2c = machine.I2C(id=0, sda=32, scl=33)




def as7343_fifo_level(sensor) -> int:
    level = sensor.r_uint8(as7343.FIFO_LVL)
    return level

# TODO: collect data into a file
def process_data(data):
    assert len(data) == 18

    print('process-data', data)

def main():

    spectral = as7343.AS7343(i2c)

    # Use FIFO
    spectral.start_measurement()
    spectral.set_integration_time(50*1000) # in us, max 182000 us
    spectral.set_measurement_time(200) # in ms


    spectral.set_illumination_current(60) # mA
    spectral.set_illumination_led(False)


    while True:
        #readings = as7343.read()
        #print(readings)

        level = as7343_fifo_level(spectral)
        #print('level-check', level, (level % 18))

        # NOTE: the level usually increments by 6, 18 channels
        # Probably there are 3 iterations of measurements
        if level == 128:
            raise ValueError('FIFO overflow')

        if level >= 18:
            # TODO: use a pre-allocated array and read into that
            data = spectral.read_fifo()
            process_data(data)

        time.sleep_ms(10)

if __name__ == '__main__':
    main()


