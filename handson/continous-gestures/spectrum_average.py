
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


