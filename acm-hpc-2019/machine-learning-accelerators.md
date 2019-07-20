
# Machine Learning Accelerators from Cloud to Edge

Luca Benini

Fransisco Conti

## Machine Learning hype curve

Bandwagon effect.
Everyone wants to be on the Deep Learning.
Establish themselves as experts.
Lots of noise.

## Neural Network fundamentals

Deep Learning networks is a generalization of a linear classifiers.

During inference.
Fundamental computation: Matrix-Vector multiplication (dot product) plus bias.
Dot product is basically just Multiply-accumulate (MAC).
=> 90-99% of computation goes to MAC. 

During training.
Regularization is simple sum or reduction.
Loss function also simple.
Inference over training set majority of the work.
=> Also mostly MAC.

## History

1960. Neural nets proposed
1989. Convnet proposed
2011. State-of-art speech recognition
2011. State-of-art computer vision
2014. Human-level computer vision
2014. Start of DNN accelerator research

2010+ Abundance of data and compute compared to pre 1990.

## Focus
Will focus on Fully Connected Neural Networks
and Convolutional Neural Networks.
Not much on Recurrent Neural Networks and LSTM.

## CNN

Convolution operation can be seen as a sparse linear combination,
computed only over a local region. Region slides over the input.
Also use shared weights.
And usually have multiple filters, and multiple input channels

Convolutions are independent.
Can be processed in parallel.
If we have enough processors, theoretically do it in a single shot.

With multiple inputs, need to do the same computation on each image.
Can be done in parallel. Batching.

CNN computation requires a lot of indicies.
Iteration over. Image position. Kernel position. Input channel. Output channel. Image.
Primiarily a huge MAC.

Can be written as a 7-layer for-loop. But there are no data-dependencies!

Mostly used activations are ReLu. Very simple operation.
Max or average pooling operation also very simple.

Batch Normalization keep activation sizes down.
Important to be able to do quantization.


Multi-megabyte weights.
Multi-giga operations.
Algorithmic improvements are being done.
But general trend is still bigger networks. Compute and weights.
Being applied to more difficult problems.

Image classification is considered a solved problem.
ImageNet a basic benchmark.

## Kernel computation

Single input. Matrix-Vector multiply.
Batching input. Matrix-Matrix multiply.
Maxtrix-Matrix computation very common.
Optimized GEMM versions exists.

Can transform CONV also to matrix-matrix.
Toeplitz operator.
Toeplit matrix (has redundant data).
Blows up the memory size.
Memory bandwidth challenge.
Fastest when using GPUs.

## Strassen
Can reduce multiplications, but gives more additions.
Whether it makes sense on low-level depends on the hardware.
Better for example on FPGA.
Lower asymptotic complexity.
Reduces numerical stability, and requires significantly more memory.

## Winograd
For convolutions. Very similar to Strassen.
Allows to reduce muliplications, but gives more additions.
Has been used for traditional linear algebra.
1D winograd be nested.
2D winograd for 2x2 and 3x3 reduces multiplications by 2.25x 
Used by Nervana (Intel).
Practical speedups in VGG around 1.8-2.0x for most layer.
Overall 13% speedup over already optimized CUDA GEMM.
Downside: Each filter size has different code. Less regular.

## FFT Flow

n^3
n*log(n) + n^2

Need to expand.
Frequency domain matrices are complex.
FFT bad memory access patterns. 
Requires much more memory and bandwidth.
Does not pay off for small filters.

Right now. FFT is not applied in hardware right now?


## Pruning
Removing near-zero weights.
Remove neurons that never activate.

Early work. Han, NIPS'15.
AlexNet. Conv 3x reduction, FC 10x.
Iterative pruning. Prune then retrain (with 0 constraint).
Sometimes could even get better results than unprune network.
However, modern networks have less FC/redundancy.

## Compression
Store weights in compressed form.

Several companies trying to differeniate using
hardware memory compression for neuralnetworks.

## Compact networks


## Reduced bitwidth

## Hardware persptive on CNN
MAC.
filter weights.
fmap activation.
partial sum.
-> outputed partial sum.
3 inputs, 1 data output.
2 operations.
4/2 memory/operation ratio.
Problem. Low arithmetic complexity. Memory bound.

1 MAC. 20 pJ energy. 1 cycle at 1 Ghz.

Need a local memory hierarchy. On-chip.
If everything can be stored in local memory, then it is easy.

## Data reuse
Full control over the computational schedule.
Want to beat (computation unaware) caches.
Schedule computations in order to maximize data reuse.

Strategies

- Convolutional reuse.
- Fmap reuse.
- Filter reuse.

Which one is best depends on relationship between input sizes, kernel sizes.

## Tuning CPU for CNN
Starting from a regular CPU. Specialize for CNN.
Proposals for all mainstream ISAs to extend for this.

Ex. RISC-V. 4 stage.

## Hardware loop
aka Zero-overhead-loop.

Move inner loop from software to hardware.
Beneficial for small loop.
SW don't need condition check, jump.
Or manipulate loop counter.
More predictable branching.
State-machine in hardware does the same.

## Bit manipulation
Useful for binazined neural networks.


## Dot product SIMD
Inference often done with 8-bit precision.
4x improvement in memory bandwidth.
Baseline. 11 cycles/output.
HW loop. 5 cycles/output.
Packed SIMD. 1.25 cycles/output
=> 9x improvement

Adds 40% gatecount to a very simple CPU.

## State-of-the-art CNN accelerator

FSD chip by Tesla.
Announced some months ago.
Tesla uses a full NN-based pipeline for autonomous driving.
99% convolutions.
Replaces NVidia hardware.

System on Chip

- 12 ARM cores
- GPGPU units
- NN accelerator

30 Gops per inference. 60 times per second.
1 Teraops/second.

32bit mult -> 8 bit mult. 20x energy efficiency.
Mixed precision.
NN hardware has 8bit mul, 32 bit accumulate.

On-die SRAM for the biggest single layer can fit. 32 MB.
96x96 MAC units.
Massive SIMD. 5-7 instructions. Working on many K data items.

144 TOPS. Versus 21 TOPS for best GPGPU.
4 TOPS/watt. 14 nm architecture.

## Compression

Non-uniform distribution of.
Entropy-based compression.

## Systolic array
Array of processors that communicate only locally.
Used in Google TPU.
Multi-chip is being considered.

## Minimum energy operation
Find the ideal voltage/frequency that minimize energy.
Great when one can scale by parallism.
And when one can tolerate small/local errors.

## In-memory inference
Computing inside the memory blocks themselves.
Using resistors proportional to the weights.
Analog implementetion of product and summing.
Kirkoffs law.
Mitic IC.
HOT. Skeptical. But doing some research on this.

## Binary networks
Ultra-low quantity networks.
Avoids multiply.
Hard to train!

Quentin. XNE-accelerated microcontroller.
Super efficient.
50 fJ/ops possible! Possible to do 100 TOPS/watt.

