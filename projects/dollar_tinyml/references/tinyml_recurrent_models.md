
# Tiny RNN alternatives

Embedded Gated Recurrent Unit (eGRU)
Minimal Gated Unit (MGRU).
FastGRNN
TinyEatsGRU
Single-tunnelled gated re-current unit (Sitgru)
Light-Gated-GRU (Li-GRU)
The Light-Gated-GRU
(Li-GRU) is proposed by [12], which removes the reset gate
and developes a single-gate RNN

#### An Ultra-low Power RNN Classifier for Always-On Voice Wake-Up Detection Robust to Real-World Scenarios
https://arxiv.org/abs/2103.04792
CEA-Leti, Université Grenoble Alpes
Hardy and Badets
Memory footprint of 0.52 kB, 1072 weights at 4 bits.

> The recursive nature of RNN is another advantage for efficient hardware implementation
> We only need to store and update the hidden state from one cycle to the other

16 first order bandpass filters, center frequencies from 100 to 7,000 Hz with Q=4, regularly spaced over a logarithmic scale.

Also tested simplified version of GRU, called Minimal Gated Unit.
Did not use biases.
Used a max pooling loss function.

Quantizes both weight and activations, down to 4-bits.
Uses an training integrated, multi-step quantization scheme.

Uses hard_sigmoid and hard_tanh that are piecewise linear.


#### Sitgru: single-tunnelled gated re-current unit for abnormality detection
https://arxiv.org/abs/2003.13528


#### Tiny Eats: Eating Detection on a Microcontroller

https://arxiv.org/abs/2003.06699


Hybrid of the traditional GRU and eGRU to make it small and fast enough to fit on the Arm Cortex M0+,
with comparable accuracy to the traditional GRU.
Utilizes only 4% of the Arm Cortex M0+ memory and identifies eating or non-eating episodes with 6 ms latency and accuracy of 95.15%.

8 bit quantized weights.

Shifted soft-sign (ς) activation function in place of sigmoid activation function
for the update and reset gates.
A regular soft-sign is used in place of tanh activation functions for candidate state (as proposed by eGRU cell).
softsign: f(x) = (x / (abs(x) + 1))

Down-sampled the raw sound data to 500 Hz.
4 second windows, 128 FFT bins.
Weighted binary-cross entropy.

Implemented quantization-aware training in PyTorch. 8 bits for weights.

Cortex M0+ with 32 KB RAM and 256 KB FLASH memory.
FFT used 9% (23 KB) of FLASH.
GRU used 12 KB of FLASH.
Takes 6 ms to execute one sample (a 4 seconds??).

#### An Optimized Recurrent Unit for Ultra-Low-Power Keyword Spotting (eGRU)
2019.
eGRU.

eGRU model is only of 3kB in size

Only 20 citations??

#### FastGRNN: A Fast, Accurate, Stable and Tiny Kilobyte Sized Gated Recurrent Neural Network
https://arxiv.org/abs/1901.02358

Over 200+ citations

Enforcing FastGRNN’s matrices to be low-rank, sparse and quantized led to a minor decrease in the prediction accuracy
but resulted in models that could be up to 35x smaller and fit in 1-6 Kilobytes for many applications.
For instance, using a 1 KB model, FastGRNN could match the prediction accuracies of all other RNNs at the task of recognizing the "Hey Cortana" wakeword.

FastGRNN can be seen as a natural simplification of UGRNN
wherethe RNN matrices are reused within the gate,
and are made low-rank, sparse and quantized so as to compress the model.

https://github.com/microsoft/EdgeML/blob/master/c_reference/src/quantized_fastgrnn.c

#### Capacity and trainability in recurrent neural networks
https://arxiv.org/abs/1611.09913

2016
ICLR 2017

200+ citations

#### 
https://arxiv.org/abs/1603.09420

2016
Minimal Gated Unit (MGU)
300+ citations

#### Compact recurrent neural networks for acoustic event detection on low-energy low-complexity platforms
Trento, Italy

https://arxiv.org/abs/2001.10876

Used VGGish.

68% accuracy in recognition on Urbansound8k
inference time of 125 ms for each 1 second of the audio
and power consumption of 5.5 mW in just 34.3 kB of RAM.

Tested using CMSIS-NN convolutions.
Was only able to get 2.2x speedup, compared to theoretical 4x.
Could not parallelize first layer because it only has 1 channel, and the CMSIS-NN optimization requires channels to be multiple of 4.
In general saw that practical MOPS were below theoretical numbers.
Best case for a layer was 53.44 MOPS, still far from 80 MOPS.

Quite comparable to https://github.com/jonnor/ESC-CNN-microcontroller


### FFT size

RISC-V




