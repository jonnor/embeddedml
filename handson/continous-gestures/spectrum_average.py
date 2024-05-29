
"""
One way of compressing a frequency spectrum from FFT into a smaller set is to average consequctive bins
Simpler alternative to mel-spectrogram. Which uses bands spaced according to Mel scale, and weighting the FFT bins accordingly 
Averaging has no parameters to store, and only one hyper-parameter - how many bins to merge / end up with.

Notably done in the "TinySpeech" examples in Tensorflow


Other examples:

https://ashishware.com/2024/05/20/pipicospeech/
CircutPython tinyspeech implementation.

Averages consequtive sections of FFT bins
Using ulab.mean
Could be a reference implementation

Other notes on the system

Not clear whether it runs in real-time.
Sampling does not seem to be syncronized to 8 Khz?
! seems to be entirely blocking. Cannot do anything else while listening for 1 second

! used 30 seconds to load DNN in generated .py files.
Only 1600 parameters.
Took 27 kB space after minification.
"""


import time
import math
import array

@micropython.native
def spectrum_summarize(spec, out):

    binsize = len(spec) // len(out)

    for bin in range(len(out)):
        s = 0.0
        for i in range(bin*binsize, (bin+1)*binsize):
            s += spec[i]        
            #print(bin, i)

        out[bin] = s / binsize
    

def test_spectrum():

    repeats = 100
    lengths = 64, 128, 256, 512
    out_length = 32

    for length in lengths:

        ones = array.array('f', (1.0 for _ in range(length)))
        out = array.array('f', (0.0 for _ in range(out_length)))

        a = array.array('f', ones)
        #spectrum_summarize(a, out)
        #print(out)

        start = time.ticks_us()
        for r in range(repeats):
            spectrum_summarize(a, out)
        t = (time.ticks_diff(time.ticks_us(), start) / repeats) / 1000.0 # ms
        print('Summarize', length, t)


if __name__ == '__main__':
    test_spectrum()


