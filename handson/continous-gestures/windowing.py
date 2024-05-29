
import time
import math
import array

# Hann
# Welch
# Triangular

def triangular_float(data):

    length = len(data)
    half = length // 2

    for i in range(length):
        x = data[i]
        # Barlett variation L==N
        c = 1 - math.fabs((i - half) / float(half) )
        data[i] = c * x

def welch_fixed_float(data):

    # TEMP: convert to q15
    d = array.array('h', (int(32767 * x) for x in data))

    welch_fixed(d)

    # TEMP: convert back to float
    for i in range(length):
        data[i] = float(d[i]) / 32767

@micropython.native
def welch_fixed(data):
    """
    Welch window function.
    Fixed-point implementation for int16/q15
    """

    length = len(data)
    half = length // 2

    QMAX = 8192

    for i in range(length):
        # a -1.0 => 0.0 => +1.0
        a = (QMAX*(i - half)) // (half) 

        # c 0.0 => 1.0 => 0.0
        c = ((QMAX*QMAX) - (a*a))//QMAX # scaling factor
        #print('a', float(a)/QMAX, float(c)/(QMAX))

        x = data[i]
        o = (c * x) // QMAX
        data[i] = o

def welch_float(data):

    length = len(data)
    half = length // 2

    for i in range(length):
        x = data[i]
        a = (i - half) / float(half)
        c = 1 - a**2
        #print(i, c)
        data[i] = c * x

def hann_float(data):
    length = len(data)
    PI2 = 2.0*math.pi

    for i in range(length):
        c = 0.5 * ( 1 - math.cos(PI2*i/length) )
        x = data[i]
        data[i] = c * x


# TODO: implement these for 16 bit integers. Which is what our audio is in

def test_window():

    repeats = 1000
    length = 1*256

    ones = array.array('f', (1.0 for _ in range(length)))

    # Hann
    a = array.array('f', ones)
    start = time.ticks_us()
    for r in range(repeats):
        hann_float(a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('Hann', t)

    # Welch floating point
    a = array.array('f', ones)
    start = time.ticks_us()
    for r in range(repeats):
        welch_float(a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('Welch(float)', t)

    # Welch fixed-point
    a = array.array('f', ones)
    a = array.array('h', (int(32767 * x) for x in a))
    start = time.ticks_us()
    for r in range(repeats):
        welch_fixed(a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('Welch(fixed)', t)


    #trig = array.array('f', ones)

    #welch_fixed_float(welch)

    #print(welch)
    #triangular_float(trig)
    #print(trig)

if __name__ == '__main__':
    test_window()
