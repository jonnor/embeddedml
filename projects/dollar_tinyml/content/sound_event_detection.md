
# Audio Machine Learning inference

TLDR: 
Theoretically possible on Puya PYF003xx6.
Need custom mel spectrogram implementation.

## Applications

For speech, the relevant tasks would be

- Voice Activity Detection. Determine if someone is speaking or not. Usually pre-processing for speech recognition.
- Keyword Spotting
- Speech Command. Detecting 

Outside of the world of speech there are, though these are more varied and may individually be a bit more niche.
Some examples I have experience with would be

- Environmental Sound Classification for Noise Monitoring
https://github.com/jonnor/ESC-CNN-microcontroller
- Gunshot counting for Noise Monitoring
https://www.youtube.com/watch?v=tklZSUUwcjs&t=2s
- Counting beans cracking during coffee bean roasting.
https://www.youtube.com/watch?v=muZY1eCke40
- Counting bubbles during fermentation for beer/wine brewing
https://www.youtube.com/watch?v=JrhsFfCOL-s


## Feature extraction: Mel spectrograms

Standard.

## Requirements

The Puya PYF003xx6 only has 4 kB RAM total.
This needs to fit both the audio preprocessing, the machine learning model,
as well as drivers and general system code.

Would like to have the audio preprocessing take 1 kB RAM.
Or at the very least below 2 kB.
This leaves another 1-2 kB RAM for the Machine Learning model.

TODO: include buffer size calculations

Audio buffer
FFT working buffers
Output buffer


## Mel spectrogram implementation with CMSIS DSP

CMSIS-DSP provides optimized code for ARM Cortex M devices.
https://github.com/ARM-software/CMSIS-DSP

This includes a lot of useful primitives, such as FFT.
The library has good support for fixed-point operations, both 32 bit and 16 bit wide datatypes.
This is very important for Cortex M0+ devices, which does not have a hardware FPU.
16 bit also saves 2x the RAM over 32 bit, which will be critical with only having 4 kB RAM total.

CMSIS-DSP has support for Mel Frequency Cepstrum Coefficients (MFCC).
However there are no functions to only get the mel spectrogram.

During testing, I also uncovered that the FFT support always use 8192 coefficients.
This is over 32 kB of FLASH usage, which is more than the total FLASH available.

Open issue about this. Since August 2021. Acknowlegded, but to fix yet
https://github.com/ARM-software/CMSIS-DSP/issues/25
So we will need to generate our own FFT tables.

Also need to generate mel tables.

## Kilobyte sized Neural Networks

Proven: RNNs

Unproven: DCT + MLP
Unproven: MLP frame-wise + MLP across frames

4 kB RAM total.
1-2 kB RAM for ML model

CMSIS-NN supports LSTM, but not GRU

FIXME: add issue in emlearn for recurrent support, LINK here 

TODO: include bit of info on efficient RNNs

## 

Some usecases may be solvable with a MLP.
? any proof of this ?

