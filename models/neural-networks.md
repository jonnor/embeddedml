

References

* [Neural-Networks-on-Silicon](https://github.com/fengbintu/Neural-Networks-on-Silicon).
Also has a large section on Model Compression papers for Neural Networks.
* [Embedded-Neural-Network](https://github.com/ZhishengWang/Embedded-Neural-Network).
Large collection of papers for model compression, and for targeting HW acceleration.

Convolutional Neural Networks.

Much more compact models than fully connected for spatial-patterns.


* [Convolutional Neural Networks for Visual Recognition](http://cs231n.github.io/convolutional-networks/).
Explains FC->CONV equivalence, Layer Sizing Patterns,
Generally early layers have few kernels, many pixels (generic features).
Late layers many kernels, few pixels (specific features).
A fully connected (FC) layer can be converted to a CONV layer.
This allows to reduce the number of passes needed over the input,
which is more computationally effective.
Several layers of small kernels (3x3) is more expressive than bigger kernel (7x7),
because they can combine in non-linear ways thanks to activation functions.
Also requires less parameters.

Optimizing CNNs

* [convolution-flavors](https://github.com/gplhegde/convolution-flavors).
Kernel to Row an Kernel to Column tricks save memory.
Also has Vectored Convolution, 1D Winograd Convolution are computationally faster.
* ResNet use stride instead of pooling layers to reduce size. Less computations?
* Grouped convolutions. Not convolving (output of) entire past layers, but just subsets.
Allows to eliminate redundant computations.
https://github.com/ShichenLiu/CondenseNet - approx twice as efficient as MobileNets

### Kernel dictionaries

Use a fixed set of kernels in a CNN or convolutional feature-map extractor.
Store their index instead of individual weights?
To reduce weight storage size for big networks.

Kernel weights 3x3 @ 8 bit = 72 bits.
Kernel map index: 32-256kernels: 5-8 bit.
Approx factor 10x reduction.

Can be done using vector quantization or clustering on the CNN weights.

References

* Clustering Convolutional Kernels to Compress Deep Neural Networks. Sanghyun Son. ECCV 2018.
From a pre-trained model, extract representative 2D kernel centroids using k-means clustering.
Each centroid replaces the corresponding kernels. Use indexed representations instead of saving whole kernels.
Applied to ResNet-18. Outperforms its uncompressed counterpart in ILSVRC2012 with over 10x compression ratio.
3.3 Accelerating convolution via shared kernel representations. Rewriting multiple shared convolutions to Add-then-conv.
3.4 Transform invariant clustering. Vertical,horizontal flip, 90 degree rotation.
Only 32 centroids required for VGG-16 to get reasonable accuracy.
Fig. 5: The 16 most(Top)/least(Bottom) frequent centroids.

### Stacking kernels


* Learning Separable Fixed-Point kernels for Deep Convolutional Neural Networks. Sajid Anwar.
Approximate the separable kernels from non-separable ones using SVD.
Separable. For a K x K filter, the count of weights is reduced from K*K to K+K and the speedup is (K**K)/2K.

### Transfer learning
* DeCAF: A deep convolutional activation feature for generic visual recognition.
DeCAF layers taken from a general task, plus SVM/LogisticRegression training outperform existing state-of-the-art.
* CNN features off the shelf: an astounding baseline for recognition. Pre-trained CNN plus SVM.
"SIFT and HOG descriptors produced big performance gains a decade ago
and now deep convolutional features are providing a similar breakthrough for recognition"
"In any case, if you develop any new algorithm for a recognition task,
it **must** be compared against the strong baseline of generic deep features + simple classifier"

Could one try well-known normalized kernels, instead of learning them?
Ex: Sobel edge detectors, median/gaussian averaging etc.

Could it give performance benefits to flatten a deep model?
Ie use a deep model, compute typical activations for the different layers,
mimick these flat convolutional kernels. Teacher-student type learning.

### Other kernel learning methods
Could one learn CNN kernels using greedy selection of sets of N kernels?

Layer-wise greedy learning can be done. Can be unsupervised or supervised.
Goes back to Y Bengio, 2007. Not so popular in 2015, after ReLu etc improved.
Can still be beneficial for datasets with small amount of labeled samples.
[1](https://stats.stackexchange.com/questions/232616/is-greedy-layer-wise-training-of-deep-networks-necessary-for-successfully-traini)
Especially unsupervised pre-training/initialization, with supervised fine-tuning using back-propagation.
Stacked Autoencoders is one approach. [1](http://ufldl.stanford.edu/wiki/index.php/Stacked_Autoencoders)

[A pre-training strategy for convolutional neural network applied to Chinese digital gesture recognition](https://ieeexplore.ieee.org/document/7586597).
Principal Component Analysis (PCA) is employed to learn convolution kernels as the pre-training strategy.
Called PCA-based Convolutional Neural Network (PCNN).

Gabor filters

* [GaborCNN](https://ieeexplore.ieee.org/document/7726188). 2016. GaborCNN.
Convolutional neural network combined with Gabor filters for strengthening the learning of texture information.
81.53% on ImageNet.
* "Informative Spectro-Temporal Bottleneck Features for Noise-Robust Speech Recognition". 2013.
Uses Gabor filters for feature extraction. On Power-normalized spectrogram.
Filters selected using sparse PCA. Multi-layer-perceptron used, pretrained with Restricted Boltzman Machine.
* "Robust CNN-based Speech Recognition With Gabor Filter Kernels". 2014.
Gabor Convolutional Neural Network (GCNN). Incorporates Gabor functions into convolutional filter kernels.
Gabor-DNN features. 
Power-normalized spectrum (PNS) instead of mel-spectrogram.
Gammatone auditory filters equally spaced on the equivalent rectangular bandwidth (ERB) scale.
Medium-duration power bias is subtracted, where the bias level calculation was based on the
ratio of arithmetic mean and geometric mean (AM/GM ratio) of the medium duration power.
A power nonlinearity with an exponent of 0.1 replaces the logarithm nonlinearity used for compression.
* "".
Gabor Convolutional Networks (GCNs).
Convolutional Gabor orientation Filters (GoFs). Learned convolution filters modulated by Gabor filter. 
Performs slightly better than ResNet with slightly fewers trainable parameters.

Q. When transfer learning on CNNs, can one transfer kernels from different models/architectures.
SubQ. Do kernels in different CNNs tend to be similar? Cluster...

### Model compression

* [Pruning Convolutional Neural Networks for Resource Efficient Inference](https://openreview.net/forum?id=SJGCiw5gl&noteId=SJGCiw5gl). ICLR 2017. Prunin criterion based on Taylor expansion that approximates the change in the cost function induced by pruning network parameters.
Focus on transfer learning. Pruning large CNNs after adaptation to fine-grained classification tasks.
Demonstrates superior performance compared to other criteria, e.g. the norm of kernel weights or feature map activation.
* [Structural Compression of Convolutional Neural Networks Based on Greedy Filter Pruning](https://arxiv.org/abs/1705.07356).
* "Compressing Convolutional Neural Networks in the Frequency Domain". Wenlin Chen.
Called FreshNets. Uses HashedNets for FC parts. Evaluated at 1/16 and 1/64 compression.
* [CNNpack: Packing Convolutional Neural Networks in the Frequency Domain](https://papers.nips.cc/paper/6390-cnnpack-packing-convolutional-neural-networks-in-the-frequency-domain.pdf). Yunhe Wang. NIPS 2016. 41 citations.
Treat convolutional kernels as images. Decompose each kernel into common parts (ie cluster centers),
and residual (unique to the kernel).
A large number of **low-energy frequency coefficients** in both parts can be discarded to
produce high compression without significantly compromising accuracy.
Relax the computational burden of convolution operations in CNNs by linearly
combining the convolution responses of discrete cosine transform (DCT) bases.
Method: kernel coefficients -> DCT -> k-means clustering -> l1 shrinkage -> quantization -> Huffman -> Compressed Sparse Row.
For similar performance, 30-40x compression on AlexNet/VGG16, 10-25x speedup. 13x compression on ResNet50. !!

### Neural Architecture Search
For embedded almost always interested in performance under constraints,
on RAM, FLASH and CPU time / energy usage.
Of interest is to find Pareto-optimal (family of) models,
which offers the best performance/constraint tradeoff.

Large amount of literature linked from
https://www.automl.org/automl/literature-on-neural-architecture-search/

SpArSe: Sparse Architecture Search for CNNs on Resource-Constrained Microcontrollers
https://arxiv.org/abs/1905.12107v1
CNNs for 2kB RAM.

EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks
https://arxiv.org/abs/1905.11946

#### On Random Weights and Unsupervised Feature Learning
NIPS 2010.

In this paper we pose the question, why do random weights sometimes do so well?
Our answer is that certain convolutional pooling architectures can be inherently
frequency selective and translation invariant, even with random weights.
Demonstrate the viability of extremely fast architecture search by using random weights to evaluate candidate architectures,
thereby sidestepping the time-consuming learning process. Process is approximately 30x faster. 
`TODO: does this have modern citations?`

#### AutoML: Methods, Systems, Challenges
https://www.automl.org/book/
2018
Reviews state of the art

#### An Overview of Machine Learning within Embedded and Mobile Devices–Optimizations and Applications
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8271867/

Reviews methods, tools, optimization techniques and applications for constrainted embedded and mobile devices.
Methods include k-NN, HMM, SVM, GMM and deep neural networks.
For each of the methods covers some optimization schemes.

For SVM concludes that the Laplacian kernel is the most efficient, since it can be implemented with shifts.
Laplacian kernel can be used in scikit-learn by precomputing the kernel.
On a practical level the number of support vectors also impact runtime.
In scikit-learn can use the NuSVC model to constrain the number of support vectors.

#### Efficient Multi-objective Neural Architecture Search via Lamarckian Evolution
Proposes LEMONADE
https://arxiv.org/abs/1804.09081
April 2018 - Feb 2019
Bosch / Uni Freiburg

Trained on CIFAR-10, evaluted on ImageNet64x64
Accuracy versus number of parameters
Pareto optimal over NASNet, MobileNet V1. Parity with MobileNet V2
24-56 GPU days used



## Sequence modelling

[Temporal Convolutional Networks](https://arxiv.org/abs/1608.08242). Using convolutions instead of Recurrent Neural Networks.
[An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling](https://arxiv.org/abs/1803.01271).

## Quantized Neural Networks

Using integer quantization, typically down to 8-bit. Reduces size of weights, allows to use wider SIMD instructions.
Most interesting for low, when applied to already-efficient deep learning architectures. Examples are MobileNet, SqueezeNet.
In microcontrollers, ARM Cortex M4F and M7 can do SIMD operations with 4x 8-bit integers.

Papers

* [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](https://arxiv.org/pdf/1712.05877.pdf).
Paper on the quantization supported in TensorFlow Lite.
Evaluated on Accuracy versus Latency tradeoff. Tested on Qualcomm Snapdragon 835 LITTLE. Using ReLU6 non-linearity. Primarily 8-bit arithmetics, 32-bit for some parts.
* Papers are expected from CVPR 2018 On-Device Visual Intelligence Challenge (June 2018),
competition focused on improving accuracy/latency tradeoff.


Blogposts

* [Why are Eight Bits Enough for Deep Neural Networks?](https://petewarden.com/2015/05/23/why-are-eight-bits-enough-for-deep-neural-networks/)
* [What I’ve learned about neural network quantization](https://petewarden.com/2017/06/22/what-ive-learned-about-neural-network-quantization/)
* [How to Quantize Neural Networks with TensorFlow](https://petewarden.com/2016/05/03/how-to-quantize-neural-networks-with-tensorflow/)
Allows to quantize in feedforward, but keep backprop as full precision floats.

Software

* [gemmlowp](https://github.com/google/gemmlowp). Low-precision General Matrix Multiplication.
C++ library for optimized GEMM using 8-bit integers, with 32 bit accumulator.
Can utilize SSE4,NEON for SIMD. Seems to run on Cortex M.
Well-documented archiecture and implementation of the quantization.

## Binarized Neural Networks

Bitwise arithmetic packed into integer representations.
Decreases weights storage drastically.
Implementable efficiently on constrained hardware (only fixed-point units).
Also called BNN, Binary Neutral Network, and XNOR neural network. 

References

* [Introduction](https://software.intel.com/en-us/articles/accelerating-neural-networks-with-binary-arithmetic)
* Paper: [Binarized Neural Networks: raining Neural Networks with Weights and Activations Constrained to +1 or −1](https://ai.intel.com/wp-content/uploads/sites/53/2017/06/1602.02830v3.pdf)
* eBNN. Paper: [Embedded Binarized Neural Networks](http://www.eecs.harvard.edu/~htk/publication/2017-ewsn-mcdanel-teerapittayanon-kung.pdf).
Runs MINST with 95% accuracy in under 50ms on Intel Curie. 32bit, 16KB RAM, 32MHz.
Reorders computation compared to BNN to only need a single floating point intermediate value, instead of one per layer.
[Code](https://gitlab.com/kunglab/ddnn). Python module which generates a C header, plus C library.
* [Deep Learning Binary Neural Network on an FPG](https://web.wpi.edu/Pubs/ETD/Available/etd-042717-145953/unrestricted/sredkar.pdf).
332,164 images per second with 85% accuracy on CIFAR-10.
* [Accelerating Binarized Neural Networks: Comparison of FPGA, CPU, GPU, and ASIC](http://jaewoong.org/pubs/fpt16-accelerating-bnn.pdf)
* [YodaNN: An Architecture for Ultra-Low Power Binary-Weight CNN Acceleration](https://arxiv.org/abs/1606.05487).
61.2TOps/sec/Watt at 900uW and 1TOps/sec/watt at 1.2v. 

Another alternative is binary shift networks, which replaces multiplications with bitshifts.


## Neural network inference optimization

* [nn_dataflow](https://github.com/stanford-mast/nn_dataflow). Energy-efficient dataflow scheduling for neural networks (NNs),
including array mapping, loop blocking and reordering, and parallel partitioning.
* [Sparse-Winograd-CNN](https://github.com/xingyul/Sparse-Winograd-CNN).
Efficient Sparse-Winograd Convolutional Neural Networks paper. ICLR 2018.
* [wincnn](https://github.com/andravin/wincnn).
Simple python module for computing minimal Winograd convolution algorithms for use with convolutional neural networks.
"Fast Algorithms for Convolutional Neural Networks" Lavin and Gray, CVPR 2016.
* [Tencent/FeatherCNN](https://github.com/Tencent/FeatherCNN).
High performance inference engine for convolutional neural networks.
For embedded Linux and mobile, especially ARM processors.
* [CNN-Inference-Engine-Comparison](https://github.com/HolmesShuan/CNN-Inference-Engine-Quick-View).
Overview of CCN inference engines, and performance.
Shows MobileNetV1 at 60ms on 2-core 1.8Ghz Cortex-A72, ResNet-18 in 200ms.


## MicroNets
https://arxiv.org/abs/2010.11267

> The CMSIS-NN CONV 2D kernel is substantially faster when
> the number of input and output channels are divisible by four

Used differentiable NAS (DNAS) (Liu et al., 2019) to design specialized MCU models to target
TinyMLperf tasks.

Keyword spotting, Acoustic Anomaly Detection (DCASE2020 Task2)

Models, but not training code, published to https://github.com/ARM-software/ML-zoo

Designed for execution with TensorFlow Lite for Microcontrollers.


