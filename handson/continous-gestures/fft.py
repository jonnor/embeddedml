
# https://github.com/thiagofe/ulab_samples
# has bechmarks for FFT
# 1024 samples, 2.0 ms

# https://github.com/fakufaku/esp32-fft/blob/master/performance/performance.csv
# 1024	0.971210 ms

# https://espressif-docs.readthedocs-hosted.com/projects/esp-dsp/en/latest/esp-dsp-benchmarks.html
# 75547 to 172664 samples
# 0.31 to 0.73 ms @ 240 Mhz

# How would emlfft stack up with these?
# Want o at least match ulab performance

# https://mecha-mind.medium.com/fast-fourier-transform-optimizations-5c1fd108a8ed
# pre-computed bit-reversal as a look up table
# computed without recursion, using a bottom-up approach
# example code in Python
# !! uses eval to get an interger from strings? 

import math
import cmath

import time
import array

try:
    import ulab
    from ulab import numpy
    pass
except ImportError as e:
    print(e)

try:
    import numpy
    import numpy.fft
except ImportError as e:
    print(e)

import emlfft

def fft_ulab(a):
    real, _ = numpy.fft.fft(a)
    return real


def make_two_sines(f1 = 2.0, f2 = 20.0, sr = 100, dur = 1.0):
    np = numpy

    t = np.linspace(0, 1, num=int(dur*sr))
    sig = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)

    return t, sig

def reverse_bits(index, length):

    # Compute levels = floor(log2(n))
    levels = 0
    temp = length
    while temp > 1:
        temp = (temp >> 1)
        levels +=1

    result = 0
    x = index
    for i in range(levels):
        result = (result << 1) | (x & 1)
        x = (x >> 1)

    return result

class FFTPreInplace:

    def __init__(self, length):

        self.length = length
        self.bit_reverse_table = array.array('h', (reverse_bits(i, length) for i in range(length)))
        self.cos_table = array.array('f', (math.cos(2.0*math.pi*i/length) for i in range(length)) )
        self.sin_table = array.array('f', (math.sin(2.0*math.pi*i/length) for i in range(length)) )

    @micropython.native
    def compute(self, real, imag):
        # check inputs
        assert len(real) == self.length
        assert len(imag) == self.length

	    # Bit-reversed addressing permutation
        # does not compile with viper
        for ii in range(self.length):
            i = int(ii)
            j = self.bit_reverse_table[i]
            if j > i:
                temp : object = real[i]
                real[i] = real[j]
                real[j] = temp
                temp = imag[i]
                imag[i] = imag[j]
                imag[j] = temp

        self._compute(real, imag)

    @micropython.native
    def _compute(self, real, imag):

        cos = self.cos_table
        sin = self.sin_table
        n : int = int(self.length)

    	## Cooley-Tukey in-place decimation-in-time radix-2 FFT
        size : int = 2
        while size <= n:
            halfsize : int = size // 2
            tablestep : int = n // size

            i = 0
            while i < n:
                k : int = 0
                j = i
                while j < i+halfsize:
                    l : int = j + halfsize

                    #tpre =  real[l] * cos[k] + imag[l] * sin[k]
                    #tpim = -real[l] * sin[k] + imag[l] * cos[k]
                    # splitting these gives 25% speedup
                    c = cos[k]
                    s = sin[k]
                    #iii = 2.0*math.pi*k/n
                    #c = math.cos(iii)
                    #s = math.sin(iii)
                    r = real[l]
                    im = imag[l]
                    tpre =  r * c + im * s
                    tpim = -r * s + im * c
                    real[l] = real[j] - tpre
                    imag[l] = imag[j] - tpim
                    real[j] += tpre
                    imag[j] += tpim
                    k += tablestep
                    j += 1

                i += size

            size = size * 2


def main():

    n = 512*2
    s = [ reverse_bits(i, n) for i in range(n) ]

    sines = make_two_sines(dur=100.0)
    data = sines[0][0:n]
    imag = numpy.zeros(data.shape, dtype=data.dtype)
    assert len(data) == n

    repeat = 100

    re = array.array('f', data)
    im = array.array('f', imag)
    fft = FFTPreInplace(n)

    start = time.time()
    for i in range(repeat):
        fft.compute(re, im)
        #out = fft_optimized(data, seq)
    d = ((time.time() - start) / repeat) * 1000.0 # ms
    print('python', d)

    start = time.time()
    for i in range(repeat):
        out = fft_ulab(data)
    d = ((time.time() - start) / repeat) * 1000.0 # ms
    print('ulab', d)

    start = time.time()
    fft = emlfft.new(n)
    emlfft.fill(fft, n)
    assert len(re) == n, (len(re), n)
    assert len(im) == n, (len(im), n)
    for n in range(repeat):
        out = fft.run(re, im)
    d = ((time.time() - start) / repeat) * 1000.0 # ms
    print('emlearn', d)

if __name__ == '__main__':

    main()
