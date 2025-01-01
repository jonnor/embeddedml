

import numpy
from matplotlib import pyplot as plt
from scipy.signal import sosfreqz
from scipy.signal import iirfilter


def design_bandpass(lower=2.0, upper=5.0, sr=100, order=2):
    
    sos = iirfilter(order, [lower, upper], btype='band',
                    analog=False, fs=sr, output='sos',
                    ftype='cheby1', rp=2.0)

    return sos

def plot_bandpass(sos, lower, upper, fmin=0.1, sr=50):
    
    w, h = sosfreqz(sos, 10000, fs=sr)
    fig, ax = plt.subplots(1)
    ax.semilogx(w, 20 * numpy.log10(numpy.maximum(abs(h), 1e-5)))
    
    ax.set_title('Bandpass frequency response')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude [dB]')
    ax.axis((fmin, sr/2.0, -100, 10))
    ax.grid(which='both', axis='both')
    for f in [lower, upper]:
        ax.axvline(f, ls='--', alpha=0.5, color='black')
    return fig

