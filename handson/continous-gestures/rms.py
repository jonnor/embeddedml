
import time
import array
import math
import micropython
from ulab import numpy


def rms_python(arr):
    acc = 0.0
    for i in range(len(arr)):
        v = float(arr[i])
        acc += (v * v)
    mean = acc / len(arr)
    out = math.sqrt(mean)
    return out


@micropython.native
def rms_micropython_native(arr):
    acc = 0
    for i in range(len(arr)):
        v = arr[i]
        acc += (v * v)
    mean = acc / len(arr)
    out = math.sqrt(mean)
    return out

# object is used for "float"
@micropython.viper
def rms_micropython_viper(arr) -> object:
    buf = ptr16(arr)
    acc = 0
    l = int(len(arr))
    for i in range(l):
        v = int(buf[i])
        acc += (v * v)
    mean = float(acc) / float(l)
    out = math.sqrt(mean)
    return out


def rms_numpy(arr):
    a = numpy.array(arr)
    m = numpy.mean(a**2.0)
    return numpy.sqrt(m)


def main():
    
    #import numpy
    #inp = numpy.linspace(0, (2**15-1), 100).astype(int)
    #inp = numpy.linspace(200, 400, 10).astype(int)
    inp = [    0,   330,   661,   992,  1323,  1654,  1985,  2316,  2647,
        2978,  3309,  3640,  3971,  4302,  4633,  4964,  5295,  5626,
        5957,  6288,  6619,  6950,  7281,  7612,  7943,  8274,  8605,
        8936,  9267,  9598,  9929, 10260, 10591, 10922, 11253, 11584,
       11915, 12246, 12577, 12908, 13239, 13570, 13901, 14232, 14563,
       14894, 15225, 15556, 15887, 16218, 16548, 16879, 17210, 17541,
       17872, 18203, 18534, 18865, 19196, 19527, 19858, 20189, 20520,
       20851, 21182, 21513, 21844, 22175, 22506, 22837, 23168, 23499,
       23830, 24161, 24492, 24823, 25154, 25485, 25816, 26147, 26478,
       26809, 27140, 27471, 27802, 28133, 28464, 28795, 29126, 29457,
       29788, 30119, 30450, 30781, 31112, 31443, 31774, 32105, 32436,
       32767] * 2

    print('length', len(inp))
    repeats = 1000

    #print(repr(inp))
    a = array.array('h', inp)

    start = time.ticks_us()
    for r in range(repeats):
        p = rms_python(a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('python', t, p)

    start = time.ticks_us()
    for r in range(repeats):
        mp = rms_micropython_native(a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('native', t, mp)

    start = time.ticks_us()
    for r in range(repeats):
        vp = rms_micropython_viper(a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('viper', t, vp)

    start = time.ticks_us()
    a = numpy.array(a)
    for r in range(repeats):
        np = rms_numpy(a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('ulab', t, np)



if __name__ == '__main__':

    main()
