
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
        #w = cmath.exp(-2j*math.pi/k) # FIXNE: switch to cmath
        w = numpy.exp(-2j*numpy.pi/k)
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


def generate_swapping_constants(n):
    # This function returns the constants used with bitwise AND
    # i.e. for extracting alternate elements, then pairs of 2, then
    # batches of 4 and so on.
    swap_constants = []
    
    i = 0
    while (1 << i) <= int(n/2):
        nbits = (1 << i)
        
        p = '0'*nbits + '1'*nbits
        q = '1'*nbits + '0'*nbits

        h = len(p)

        d, r = int(n/h), n % h
        
        a = '0b' + p*d + p[:r]
        b = '0b' + q*d + q[:r]

        swap_constants += [(nbits, eval(a), eval(b))]
        i += 1

    return swap_constants

def get_bit_reversed_seq(n, m, swap_constants, nxt_power):
    seq = []
    
    for x in range(n):
        x *= (1 << (nxt_power-m))
        
        for q, a, b in swap_constants:
            x = ((x & a) << q) | ((x & b) >> q)
            
        seq += [x]

    return seq


# XXX: this takes many seconds!!
def make_sequences():
    max_bits = 32
    swap_table = []

    nbits = 1
    while nbits <= max_bits:
        swap_constants = generate_swapping_constants(nbits)
        swap_table += [(nbits, swap_constants)]
        nbits *= 2

    sequences = {}
    i = 0
    for m in range(1, 16):
        n = 1 << m
        print(n)

        while i < len(swap_table) and m > swap_table[i][0]:
            i += 1

        sequences[m] = \
            get_bit_reversed_seq(n, m, 
                swap_table[i][1], swap_table[i][0])

    return sequences

def num_bits(n):
    c = 0
    while n > 0:
        n = n >> 1
        c += 1

    return c

def fft_optimized(x, sequences):
    n = len(x)

    # n is power of 2, but sequence is from 0 to n-1
    # number of bits required is 1 minus the number of bits in n
    m = num_bits(n)-1

    return fft_bit_reversal(x, sequences[m])

import time
import array

try:
    from ulab.numpy.fft import fft as ulab_fft
    from ulab import numpy
except ImportError as e:
    print(e)

try:
    import numpy
    import numpy.fft
except ImportError as e:
    print(e)


def fft_ulab(a):
    real, _ = ulab_fft(a)
    return real

def fft_numpy(a):
    out = numpy.fft.rfft(a)
    return out

def make_two_sines(f1 = 2.0, f2 = 20.0, sr = 100, dur = 1.0):
    np = numpy

    t = np.linspace(0, 1, int(dur*sr), False)
    sig = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)

    return t, sig

def main():

    seq = make_sequences()

    n = 512
    m = num_bits(n)-1
    s = seq[m]
    print(n, m, s)

    sines = make_two_sines(dur=10.0)
    data = sines[0][0:n]

    repeat = 100

    start = time.time()
    a = array.array('f', data)
    for n in range(repeat):
        out = fft_optimized(a, seq)
    d = ((time.time() - start) / repeat) * 1000.0 # ms
    print('python', d)

    start = time.time()
    for n in range(repeat):
        out = fft_numpy(data)
    d = ((time.time() - start) / repeat) * 1000.0 # ms
    print('numpy', d)

if __name__ == '__main__':

    main()
