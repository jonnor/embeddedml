
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



# in-place, mutates X
def fft_bit_reversal(x, seq):
    n = len(seq)

    # seq : permutation of 0 to n-1 using bit reversal technique
    for i in range(n):
        seq_i = seq[i]
        x[i] = x[seq_i]

    k = 2
    
    # at each level, the even FFT lies from index i+j to i+j+u-1
    # and odd FFT lies from index i+j+u to i+j+k-1
    # merge the 2 FFTs into a single FFT from i+j to i+j+k-1
    while k <= n:
        w = cmath.exp(-2j*math.pi/k) # FIXNE: switch to cmath
        #w = numpy.exp(-2j*numpy.pi/k)
        u = int(k/2)
        
        for i in range(0, n, k):
            h = 1
            for j in range(u):
                a, b = x[i+j], x[i+j+u]
                
                x[i+j] = a + h*b
                x[i+j+u] = a - h*b
                h *= w
                
        k *= 2

    return x


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
        self.sin_table = array.array('f', (math.cos(2.0*math.pi*i/length) for i in range(length)) )

    def compute(self, real, imag):
        # check inputs
        assert len(real) == self.length
        assert len(imag) == self.length

        self._compute(real, imag)

    @micropython.native
    def _compute(self, real, imag):

        length = len(real)
        cos = self.cos_table
        sin = self.sin_table

	    # Bit-reversed addressing permutation
        for i in range(length):
            j = self.bit_reverse_table[i]
            if j > i:
                temp = real[i]
                real[i] = real[j]
                real[j] = temp
                temp = imag[i]
                imag[i] = imag[j]
                imag[j] = temp

    	## Cooley-Tukey in-place decimation-in-time radix-2 FFT
        n = self.length
        size = 2
        while size <= length:
            halfsize = size // 2
            tablestep = n // size

            for i in range(0, n, size):
                k = 0
                #print(i)
                for j in range(i, i + halfsize):
                    #print('k', k)
                    self._compute_inner(real, imag, j, k, halfsize, cos, sin)
                    # next
                    k += tablestep
            # next
            size = size * 2

    @micropython.viper
    def _compute_inner(self, real, imag, j, k, halfsize, cos, sin):
        l = j + halfsize;
        tpre =  real[l] * cos[k] + imag[l] * sin[k]
        tpim = -real[l] * sin[k] + imag[l] * cos[k]
        real[l] = real[j] - tpre
        imag[l] = imag[j] - tpim
        real[j] += tpre
        imag[j] += tpim


def main():

    n = 512
    s = [ reverse_bits(i, n) for i in range(n) ]

    sines = make_two_sines(dur=10.0)
    data = sines[0][0:n]
    imag = numpy.zeros(data.shape, dtype=data.dtype)

    repeat = 100

    a = array.array('f', data)
    i = array.array('f', imag)
    fft = FFTPreInplace(n)

    start = time.time()
    for n in range(repeat):
        fft.compute(a, i)
        #out = fft_optimized(data, seq)
    d = ((time.time() - start) / repeat) * 1000.0 # ms
    print('python', d)

    start = time.time()
    for n in range(repeat):
        out = fft_ulab(data)
    d = ((time.time() - start) / repeat) * 1000.0 # ms
    print('numpy', d)

if __name__ == '__main__':

    main()
