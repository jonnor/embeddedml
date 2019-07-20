
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


