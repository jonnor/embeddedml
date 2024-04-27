
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

# https://stackoverflow.com/a/20932062
def butter2_lowpass(f, sr):
    ff = 
    const double ita =1.0/ tan(M_PI*ff);
    const double q=sqrt(2.0);
    b0 = 1.0 / (1.0 + q*ita + ita*ita);
    b1= 2*b0;
    b2= b0;
    a1 = 2.0 * (ita*ita - 1.0) * b0;
    a2 = -(1.0 - q*ita + ita*ita) * b0;

