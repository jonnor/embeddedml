
from imu import SomeIMU

SAMPLERATE = 25
THRESHOLD = 25 
sensor = SomeIMU(i2c=...)
samples = []
while True:
    t = time.ticks_ms()
    samples.append(sensor.get_xyz())

    if len(samples) == THRESHOLD:
        process_samples(samples)
        samples = []

    # Try compensate for execution time data sampling time
    time_spent = time.ticks_diff(time.ticks_ms(), t)
    wait_time = max(1000/SAMPLERATE - time_spent, 0)
    time.sleep_ms(wait_time)



SAMPLERATE = 25
THRESHOLD = 25 # NOTE: max 75% of FIFO capacity
imu = SuperIMU2k(i2c=..., odr=SAMPLERATE)

while True:
    level = imu.get_fifo_level()
    if level >= THRESHOLD:
        samples = imu.read_fifo_data(THRESHOLD)        

        process_samples(samples) 

    machine.lightsleep(100)
