
# Model size

## Models designed to be small

* [Resource-efficient Machine Learning in 2 KB RAM for the Internet of Things](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/kumar17.pdf).
Describes Bonsai, a part of Microsoft Research Indias open-source [EdgeML](https://github.com/Microsoft/EdgeML).
Bonsay is tree-based algorithm. Relatively powerful nodes to enable short trees (reduce RAM usage).
Uses sparse trees, and the final prediction is a sum of all the nodes (path-based).
Optimization: `tanh(x) ≈ x if x < 1 and signum(x) otherwise`. Can run on Atmel AVR8
* [ProtoNN: Compressed and Accurate kNN for Resource-scarce Devices](http://manikvarma.org/pubs/gupta17.pdf).
k-Nearest Neighbor implementation. Can run on Atmel AVR8


## Model optimization

* [SeeDot](https://www.microsoft.com/en-us/research/project/seedot-compiler-for-low-precision-machine-learning/).
DSL and compiler for fixed-point ML inference on microcontrollers.
[PDLI paper](http://www.sridhargopinath.in/wp-content/uploads/2019/06/pldi19-SeeDot.pdf).
Tested on models. Bonsai, ProtoNN, and LeNet CNN.
Hardware. Arduino Uno (AVR8) and Arduino MK1000 (Cortex-M0+), FPGA.
Comparison with floating-point, TensorFlow Lite quantization, and MATLAB Coder/Embedded Coder/Fixed-point Designed .
2-20x improvements in inference time.
Also implements a fast-exponensiation trick. Schraudolph, 1999.
