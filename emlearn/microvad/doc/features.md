
# Feature extraction


## Polyphase filterbanks

Performing the STFT followed by mel-filtering mapping to a low number of bands,
might be computationally wasteful compared to a more direct implementation.
One candidate is a polyphase filterbank.

WebRTC uses 6 frequency bands, implemented using multi-rate filterbank.
It *might* be implemented using polyphase filterbank.

https://github.com/kastnerkyle/kastnerkyle.github.io/blob/master/posts/polyphase-signal-processing/polyphase-signal-processing.ipynb
Shows Python code for polyphase filterbank

> A typical rule is that filters up to around 64 taps are faster to apply in the time domain,
> while > 64 taps can typically be applied faster using an fftconvolve routine.
> This is highly platform dependent, but can serve as a decent guideline.


https://github.com/GuitarsAI/MRSP_Notebooks/blob/master/MRSP_Optimization_FilterBanks.ipynb

> Obtain a filter bank from our structure or product ....,
> which has "good" subband filters,
> i.e. a good or sufficient stopband attenuation and not much pass band attenuation.
> An example could be a desired stopband attenuation of -60dB and a pass band attenuation of less than -3dB.

Multirate Signal Processing with Python Examples - Full Course - Ilmenau University of Technology 
https://www.youtube.com/watch?v=eHZgdfDLWhU

Polyphase Filter Bank implementation in C++
https://github.com/alexranaldi/PolyphaseFilterBank


