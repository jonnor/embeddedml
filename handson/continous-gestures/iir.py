
# Butterworth is a special case of Chebychev with 0% passband ripple
# Chebychev with 0.5% passband ripple has considerably better sharper transition


# https://github.com/adis300/filter-c/blob/master/filter.c#L178
# https://github.com/edgeimpulse/inferencing-sdk-cpp/blob/master/dsp/spectral/filters.hpp
# very similar code structure
# uses A,d1,d2,w0,w1,w2 instead of familiar a,b
# original algorithm here
# https://exstrom.com/journal/sigproc/dsigproc.html
# !! the C codes there are under GNU GPL

# https://github.com/vinniefalco/DSPFilters/blob/master/shared/DSPFilters/source/ChebyshevI.cpp
# code spread over multiple functions, bit hard to understand the complete that is needed

# https://github.com/qq456cvb/cs231n/blob/master/assignment2/cs231n/.env/lib/python2.7/site-packages/scipy/signal/filter_design.py#L768
# computes in analog domain, does s->z transfer


# https://github.com/GStreamer/gst-plugins-good/blob/master/gst/audiofx/audiocheblimit.c
# more general code for Chebyshev Type I IIR biquads

# https://github.com/berndporr/py-iir-filter/blob/master/iir_filter.py
# sosfilt type implementation in pure Python

# https://www.samproell.io/posts/yarppg/yarppg-live-digital-filter/
# SOSfilt implementation in pure Python

import math
import array
import time

# https://stackoverflow.com/a/20932062
def butter2_lowpass(f, sr):
    ff = f / sr
    ita = 1.0/ math.tan(math.pi*ff)
    q = math.sqrt(2.0)
    b0 = 1.0 / (1.0 + q*ita + ita*ita)
    b1 = 2 * b0
    b2 = b0
    a1 = 2.0 * (ita*ita - 1.0) * b0
    a2 = -(1.0 - q*ita + ita*ita) * b0

    # Return in biquad / Second Order Stage format
    # to be compatible with scipy, a1 and a2 needed to be flipped??
    sos = [ b0, b1, b2, 1.0, -a1, -a2 ]

    return sos

class IIRFilter():
    def __init__(self, coefficients : array.array):
        stages = len(coefficients)//6

        self.sos = coefficients
        self.state = array.array('f', [0.0]*(2*stages))

    @micropython.native
    def process(self, samples : array.array):
        """Filter incoming data with cascaded second-order sections.
        """

        stages = len(self.sos)//6

        # iterate over all samples
        for i in range(len(samples)):
            x = samples[i]

            # apply all filter sections
            for s in range(stages):
                b0, b1, b2, a0, a1, a2 = self.sos[s*6:(s*6)+6]

                # compute difference equations of transposed direct form II
                y = b0*x + self.state[(s*2)+0]
                self.state[(s*2)+0] = b1*x - a1*y + self.state[(s*2)+1]
                self.state[(s*2)+1] = b2*x - a2*y
                # set biquad output as input of next filter section
                x = y

            # assign to output
            samples[i] = x

        return None

try:
    from ulab import numpy
    from ulab import scipy
except ImportError as e:
    print(e)
    pass

try:
    import emliir
except ImportError as e:
    print(e)
    pass


def iir_python(sos, samples):
    #out = samples.copy()
    iir = IIRFilter(sos)
    iir.process(samples)

def iir_ulab(sos, samples):
    return scipy.signal.sosfilt(sos, samples)

def iir_emlearn(sos, samples):
    iir = emliir.new(sos)
    iir.run(samples)

def main():

    cutoff = 10.0
    sr = 100
    sos = [
        butter2_lowpass(cutoff, sr),
        butter2_lowpass(cutoff, sr),
        butter2_lowpass(cutoff, sr),
        butter2_lowpass(cutoff, sr),
        butter2_lowpass(cutoff, sr),
    ]
    coeff = []
    for s in sos:
        coeff += s
    coeff = array.array('f', coeff)
    print('cc', len(coeff))

    repeats = 100000
    inp = numpy.load('sines-input.npy')

    # use array.array always
    # NOTE: accessing/setting single values of ulab arrays is very slow
    a = array.array('f', inp)

    # Pure Python
    iir = IIRFilter(sos)
    start = time.ticks_us()
    for r in range(repeats):
        #iir.process(a)
        iir_python(sos, a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('python', t)

    # ulab
    start = time.ticks_us()
    for r in range(repeats):
        #iir.process(a)
        iir_ulab(sos, inp)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('ulab', t)

    # emlearn
    start = time.ticks_us()
    iir = emliir.new(coeff)
    for r in range(repeats):
        iir.run(a)
        #iir_emlearn(coeff, a)
    t = time.ticks_diff(time.ticks_us(), start) / repeats
    print('emlearn', t)

if __name__ == '__main__':
    main()
