
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

import math

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

def plot_frequency_response(filters : dict, sr, cutoff=None):
    import scipy.signal
    import numpy
    from matplotlib import pyplot as plt

    for name, sos in filters.items():
        b, a = scipy.signal.sos2tf(sos)
        w, h = scipy.signal.freqz(b, a, fs=sr)
        plt.semilogx(w, 20 * numpy.log10(abs(h)), label=name)

    plt.title('Butterworth filter frequency response')
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.legend()
    plt.ylim(-120, 20)

    if cutoff is not None:
        plt.axvline(cutoff, color='green')
        plt.axhline(-3.0, color='green', ls='--')

    plt.show()

def main():

    sr = 100
    cutoff = 1.0

    import scipy.signal

    ref = scipy.signal.butter(2, cutoff, btype='low', analog=False, output='sos', fs=sr)
    sos = [ butter2_lowpass(cutoff, sr) ]

    print(ref)
    print(sos)
    
    plot_frequency_response({'scipy': ref, 'our': sos}, sr=sr, cutoff=cutoff)


if __name__ == '__main__':
    main()
