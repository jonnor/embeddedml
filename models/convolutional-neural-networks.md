

### Small Convolutional Neural Nets

* [SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <0.5MB model size](http://arxiv.org/abs/1602.07360). 2015.
1x1 convolutions over 3x3. Percentage tunable as hyperparameters.
Pooling very late in the layers.
No fully-connected end, uses convolutional instead.
5MB model performs like AlexNet on ImageNet. 650KB when compressed to 8bit at 33% sparsity. 
* [MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications](https://arxiv.org/abs/1704.04861). 2017.
Extensive use of 1×1 Conv layers. 95% of it’s computation time, 75% parameters. 25% parameters in final fully-connected.
Also depthwise-separable convolutions. Combination of a depthwise convolution and a pointwise convolution.
Has two hyperparameters: image size and a width multiplier `alpha` (0.0-1.0).
Figure 4 shows log linear dependence between accuracy and computation.
0.5 MobileNet-160 has 76M mul-adds, versus SqueezeNet 1700 mult-adds, both around 60% on ImageNet.
Smallest tested was 0.25 MobileNet-128, with 15M mult-adds and 200k parameters.
* [ShuffleNet](https://arxiv.org/abs/1707.01083). Zhang, 2017.
Introduces the three variants of the Shuffle unit. Group convolutions and channel shuffles.
Group convolution applies over data from multiple groups (RGB channels). Reduces computations.
Channel shuffle randomly mixes the output channels of the group convolution.
* [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://arxiv.org/abs/1801.04381). 2018
Inserting linear bottleneck layers into the convolutional blocks.
Ratio between the size of the input bottleneck and the inner size as the expansion ratio.
Shortcut connections between bottlenecks.
ReLU6 as the non-linearity. Designed for with low-precision computation (8 bit fixed-point). y = min(max(x, 0), 6).
Max activtions size 200K float16, versus 800K for MobileNetV1 and 600K for ShuffleNet.
Smallest network at 96x96 with 12M mult-adds, 0.35 width. Performance curve very similar to ShuffleNet.
Combined with SSDLite, gives similar object detection performance as YOLOv2 at 10% model size and 5% compute.
200ms on Pixel1 phone using TensorFlow Lite.
* [EffNet](https://arxiv.org/abs/1801.06434). Freeman, 2018.
Spatial separable convolutions.
Made of depthwise convolution with a line kernel (1x3),
followed by a separable pooling,
and finished by a depthwise convolution with a column kernel (3x1).
* [FD-MobileNet: Improved MobileNet with a Fast Downsampling Strategy](https://arxiv.org/abs/1802.03750). 2018.
[3 Small But Powerful Convolutional Networks](https://towardsdatascience.com/3-small-but-powerful-convolutional-networks-27ef86faa42d).
Explains MobileNet, ShuffleNet, EffNet. Visualizations of most important architecture differences, and the computational complexity benefits.
[Why MobileNet and Its Variants (e.g. ShuffleNet) Are Fast](https://medium.com/@yu4u/why-mobilenet-and-its-variants-e-g-shufflenet-are-fast-1c7048b9618d).
Covers MobileNet, ShuffleNet, FD-MobileNet.
Explains the convolution variants used visually. Pointwise convolution (conv1x1), grouped convolution, depthwise convolution.
