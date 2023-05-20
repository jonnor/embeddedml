
# Voice Activity Detection

## Problem setup

Real-time versus offline.

https://www.sciencedirect.com/science/article/abs/pii/S0885230813000533
NIST
Compares with Statistical Model (SM) based VAD and Gaussian Mixture Model (GMM) based VAD

(1) noise reduction is vital for energy-based VAD under low SNR;
(3) spectral subtraction makes better use of background spectra
than the likelihood-ratio tests in the SM-based VAD

### References

https://wiki.aalto.fi/pages/viewpage.action?pageId=151500905
Very pedagogical.
Going through the definition of the task,
the evaluation setup,
compares energy-based model with linear predictive model (autocorrelation-based),

Describes post-processing heuristics. Such as "hangover".

Features for voice activity detection: a comparative analysis
https://asp-eurasipjournals.springeropen.com/articles/10.1186/s13634-015-0277-z

## Audio interfacing

https://miniaud.io/
Supports audio input
Support audio file decoding (WAV,MP3,FLAC,Vorbis). 
Supports audio file writing (WAV only)
Supports web/Emscripten
Supports resampling (linear)
MIT

https://libsndfile.github.io/libsndfile/
Reading files
LGPL

http://portaudio.com/
MIT
