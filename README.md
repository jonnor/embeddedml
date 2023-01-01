# Machine learning on embedded devices

Focused primarily on running inference/prediction/feed-forward part on a microcontroller (or small embedded device).
Training phase can run on a standard computer/server, using existing tools as much as possible.


# State of the Art in 2019
Of ML inference on general-purpose microcontrollers.

- Deep models have efficient implementations for ARM Cortex-M. Ex: CNN and RNN in CMSIS-NN, FC in uTensor
- Some implementations available for non-neural models that *can* be used. Ex: SVM,RF,AdaBoost in sklearn-porter
- A few special-designed ML algorithms made. Ex: ProtoNN, Bonsai
- Basic tools available for converting Tensorflow models
- Keyword-spotting/wake-word on audio well established. Used in commercial products (Alexa etc)
- Human activity detecton on accelerometers.
- Computer vision is actively developed
- Lots of research and many announcements of low-power co-processors, but little on market yet

Limitations

- Neural models lacking for non-ARM micros. ESP8266/ESP32
- Non-neural models missing inference engines designed for microcontrollers
- "Small DNN" work mostly on computer vision for mobile phones (model size 1000x of uC)
- Few/no pretrained models available. Transfer learning little explored?
- Very little documentation of entire development process.
From planning, data aquisition, model design
- Best practices underdocumented (or underdeveloped?) 

Ways of advancing, make contributions

- Faster inference. Power saving, or bigger problems.
- Smaller models. Cheaper MCU, or bigger problems.
- Better accuracy on a problem. Better user experience, new usecases
- Solve a concrete usecase. Easier to deploy similar usecases
- Comparison between approaches. Microcontroller, ML model
- Libraries or tools. Lower time to market, enable more developers

# State of the Art in 2023

TODO: document



# Tools

Open-source

* [emlearn](http://github.com/emlearn/emlearn).
- [micromlgen](https://github.com/eloquentarduino/micromlgen)
* [TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers)
* [nnom](https://github.com/majianjia/nnom) - Fixed-point neural network compiler for microcontrollers.
- [nn4mc_cpp](https://github.com/correlllab/nn4mc_cpp)

Proprietary

* X-CUBE-AI for STM32

http://www.sridhargopinath.in/wp-content/uploads/2019/06/pldi19-SeeDot.pdf


# Background

## What and when to use machine learning

The defaults right now are to do conventional signal processing (no learning) in sensor,
and stream raw data to the cloud for storage and processing. Machine learning happens in the cloud.
If gateways are used, they mostly forward communication (no data processing). 

On-edge processing valueable when

* Local response needed. Autonomy
* Adaptable response needed. Over time, in context.
* Low/predictable latency needed
* Sending raw sensor data has privacy implications.
Audio, video
* Unreliable connection
* High bandwidth sensor input.
Audio, video, accelerometer/IMU, current sensor, radiowaves.
* Low bandwidth algorithm output
* Events of interest are rare
* Low energy usage needed
* Full/raw sensor data is not valuable to store
* Low cost sensor unit

Example usecases

* Predictive maintenance, using audio/vibration data
* Activitity detection for people, using audio/accelerometer data. Assistive tech, medical
* Appliance disaggregation, using aggregated power consumption data. "Non-Intrusive Load Monitoring" (NILM)
* Anomaly/change detection for predictive maintenance, using audio/vibration data, or electrical data
* Gesture recognition as human input device, using accelerometer/gyro data.
* Speech/command recognition as human input device, using microphone. Keyword/Wake-word detection
* Battery saving in wireless sensors. Normally sending day/week aggregates, on event/anomaly detection send data immediately
* Health status of animals via activity detected using accelerometer
* Monitoring eating activity using accelerometer [1](https://www.sciencedirect.com/science/article/pii/S0010482515000086)
* Environmental monitoring, using microphone to detect unwanted activity like cutting down trees
* Adaptive signalling and routing for wireless transmission in Wireless Sensor networks
* Electronic nose using arrays of MEMS detectors
* Material identification using reflecive spectrometer [1](https://hackaday.io/project/143014-compact-25-spectrometer/)

## Energy budgets

Scenarios

* Constantly on wired power
* Periodically used on battery, else plugged in
* Always/normally battery powered
* Energy harvesting. Never connected to charger, should run forever

### Energy harvesting

Energy harvesting rules of thumb:

    Outdoor light – 10mW/cm2
    Industrial temperature difference – 1-10 mW/cm2

    Industrial vibration – 100µW/cm2
    Human temperature difference – 25µW/cm2
    Indoor light – 10µW/cm2
    Human vibration – 4µW/cm2

    GSM RF – 0.1µW/cm2
    Wifi RF – 0.001µW/cm2

[AI and Unreliable Electronics (*batteries not included)](https://petewarden.com/2016/12/29/ai-and-unreliable-electronics-batteries-not-included/). 

### Wireless transmission

```
TODO: overview of typical energy requirements, for different wireless tech
TODO: overview of data transmission capacity, for different wireless tech
TODO: overview of sending range, for different wireless tech
TODO: cost (monetary) of data transmission, for different wireless techs
```

## Privacy

Doing more of the data processing locally, enables storing or transmitting privacy sensitive data more seldom.

Ref

* [Scalable Machine Learning with Fully Anonymized Data](https://adamdrake.com/scalable-machine-learning-with-fully-anonymized-data.html)
Using feature hashing on client/sensor-side, before sending to server that performs training.
_hashing trick_ is an established way of processing data as part of training a machine learning model.
The typical motivation for using the technique is a reduction in memory requirements or the ability to perform stateless feature extraction.
While feature hashing is ideally suited to categorical features, it also empirically works well on continuous features

Ideas

* In audio-processing, could we use a speech detection algorithm to avoid storing samples with speech in them?
Can then store/transmit the other data in order to do quality assurance and/or further data analysis. 


# Techniques

Roughly ordered by relevance. Should both be useful for typical tasks and efficiently implementable. 

* Decision trees, random forests
* Convolutional Neural networks (quantized)
* Binary Neural networks
* Support Vector Machines. SVM.
* Naive Bayes
* Nearest Neighbours. kNN. Reduced prototypes 

Ideas

* Metric learning. Specially HDML / Hamming Distance Metric Learning (Norouzi 2012),
since Hamming distance is very compact, and neighbours can be found fast.


Machine learning tasks

* Classification
* Regression
* Prediction
* Outlier/novelty/anomaly detection

# Introduction materials

- [Embedded.com: Applying machine learning in embedded systems](https://www.embedded.com/applying-machine-learning-in-embedded-systems)
- [Embedded.com: Transfer learning for the IoT](https://www.embedded.com/transfer-learning-for-the-iot/)

## Tree-based methods
Implemented in [emlearn](https://github.com/emlearn/emlearn).

Notes under models [tree-based](./models/tree-based.md).

## Mixture models
Implemented in [emlearn](https://github.com/emlearn/emlearn).

Notes under [models/mixtures](./models/mixtures.md).


## Naive Bayes
Implemented in [emlearn](https://github.com/emlearn/emlearn)


## Neural Networks

Notes under [models/mixtures](./models/neural-networks.md).


## Support Vector Machines

[Notes](./models/support-vector-machine.md)

## Nearest Neighbours

[Notes](./models/k-nearest-neighbours.md)


## Existing work

Projects

* [RPS-RNN](https://github.com/PaulKlinger/rps-rnn).
Small physical device that can play Rock, Paper, Scissors slightly better than chance.
Custom electronics and 3d-printed casing.
3-layer RNN running on 8-bit microcontroller, Attiny1614.

Software libraries


Neural network inference optimization

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


* [ESP-WHO](https://github.com/espressif/esp-who). Face recognition based on MobileNets, which custom CNN implementation?


* [tflite micro](https://www.tensorflow.org/lite/microcontrollers).
TensorFlow Lite for microcontrollers. Since November 2018. Supports ARM Cortex M, RISC-V and Linux/MacOS host.
* [Embedded Learning Library](https://github.com/Microsoft/ELL) by Microsoft.
Set of C++ libraries for machine learning on embedded platforms. Includes code for kNN, RandomForest etc.
Also has some node-based dataflow system in place it seems. JavaScript and Python bindings.
* [Embedded Classification Software Toolbox](https://github.com/ma2th/ecst)
* [uTensor](https://github.com/uTensor/uTensor). Export Tensorflow model to mbed/ARM microcontrollers.
128+ kB RAM and 512kB+ flash recommended.
"3-layer MLP is less than 32kB". Does not support CNNs yet. https://github.com/uTensor/uTensor/issues/99
Not supported on ESP8266/ESP32. https://github.com/uTensor/uTensor/issues/137
* [SeeDot](https://www.microsoft.com/en-us/research/project/seedot-compiler-for-low-precision-machine-learning/).
DSL and compiler for fixed-point ML inference on microcontrollers.
[PDLI paper](http://www.sridhargopinath.in/wp-content/uploads/2019/06/pldi19-SeeDot.pdf).
Tested on models. Bonsai, ProtoNN, and LeNet CNN.
Hardware. Arduino Uno (AVR8) and Arduino MK1000 (Cortex-M0+), FPGA.
Comparison with floating-point, TensorFlow Lite quantization, and MATLAB Coder/Embedded Coder/Fixed-point Designed .
2-20x improvements in inference time.
Also implements a fast-exponensiation trick. Schraudolph, 1999.

Papers

* [Resource-efficient Machine Learning in 2 KB RAM for the Internet of Things](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/kumar17.pdf).
Describes Bonsai, a part of Microsoft Research Indias open-source [EdgeML](https://github.com/Microsoft/EdgeML).
Bonsay is tree-based algorithm. Relatively powerful nodes to enable short trees (reduce RAM usage).
Uses sparse trees, and the final prediction is a sum of all the nodes (path-based).
Optimization: `tanh(x) ≈ x if x < 1 and signum(x) otherwise`. Can run on Atmel AVR8
* [ProtoNN: Compressed and Accurate kNN for Resource-scarce Devices](http://manikvarma.org/pubs/gupta17.pdf).
k-Nearest Neighbor implementation. Can run on Atmel AVR8
* [Machine Learning for Embedded Systems: A Case Study](http://www.cs.cmu.edu/~khaigh/papers/2015-HaighTechReport-Embedded.pdf)
Support Vector Machines. Target system used for auto-tunic a mobile ad-hoc network (MANET) by
earns the relationships among configuration parameters. Running on ARMv7 and PPC, 128MB+ RAM.
Lots of detail about how they optimized an existing SVM implementation, in the end running 20x faster.

Books

* [Learning in Embedded Systems](https://mitpress.mit.edu/books/learning-embedded-systems), May 1993.
* [TinyML: Machine Learning with TensorFlow on Arduino, and Ultra-Low Power Micro-Controllers](https://www.amazon.com/TinyML-Learning-TensorFlow-Ultra-Low-Micro-Controllers/dp/1492052043/ref=sr_1_13?keywords=machine+learning+sound&qid=1562670977&s=books&sr=1-13). Planned: January, 2020.


Blogposts

* [Why the Future of Machine Learning is Tiny (devices)](https://petewarden.com/2018/06/11/why-the-future-of-machine-learning-is-tiny)
Tiny Computers are Already Cheap and Everywhere. Energy is the Limiting Factor.We Capture Much More Sensor Data Than We Use.
* [embedded.com: Bringing machine learning to the edge](https://www.embedded.com/electronics-blogs/say-what-/4460873/Bringing-machine-learning-to-the-edge--A-Q-A-with-Neurala-s-Anatoli-Gorshechnikov-)
Predictions are much lower bandwidth than the raw sensor data (e.g. video)
It allows for local adaptation in the AI logic (L-DNN)
It achieves lower latency between observed event and action resulting from AI logic
"the most important question is what is the least amount accuracy and computation complexity we can do
while still delivering the business value?"
Top mistake: "Continuing with the top down approach ‘let’s make it perform the task first and then squeeze it on device`
instead of switching to bottom up ‘let’s make it run on device and fulfill all hardware constraints first,
and then tune it for the task at hand’."
* [How to run deep learning model on microcontroller with CMSIS-NN](https://www.dlology.com/blog/how-to-run-deep-learning-model-on-microcontroller-with-cmsis-nn/). Why run deep learning model on a microcontroller?
    Sensitive data gets to the cloud, photos, and audio recordings.
    The company who sells this may charge a service fee to use its service and even worse sell your private data.
    It won't work without the network connection to the server.
    Data traveling back and forth between the device and server introduces lag.
    Require network and wireless hardware components on the circuit design which increase the cost.
    It might waste bandwidth sending useless data.
* [eetimes: AI at the Very, Very Edge](https://www.eetimes.com/document.asp?doc_id=1334918#).
Report from first TinyML meetup in BayArea.



# Applications

## [Human Activity Recognition](./applications/human-activity-recognition.md)
## [Gesture recognition](./applications/gesture-recognition.md)


## Vibration analysis
Often used for 'machine condition' analysis, especially for rotating machines.

* [Fundamentals of Vibration Measurement and Analysis Explained](http://www.lifetime-reliability.com/free-articles/maintenance-management/Fundamentals_of_Vibration_Measurement_and_Analysis_Explained.pdf), explains how to capture data, process it to commonly used features etc
* [Beginning Vibration Analysis](http://www.vibranalysis.co.za/ctc/pdf/pubTechPapers/01-Beginning%20Vibration%20Analysis.pdf),
page 82+ shows data for some problematic cases

## Predictive maintenance

[NASA Prognostics Data Repository](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository).
Collection of datasets for operational and failed systems. Thermal, vibration, electronical


## Computer vision

Motivation: 

"Recent studies show that the latencies to upload
a JPEG-compressed input image (i.e. 152KB) for a single inference
of a popular CNN–“AlexNet” via stable wireless connections with
3G (870ms), LTE (180ms) and Wi-Fi (95ms), can exceed that of DNN
computation (6∼82ms) by a mobile or cloud-GPU."
Moreover,the communication energy is comparable with the associated DNN computation energy.

Y. Kang, J. Hauswald, C. Gao, A. Rovinski, T. Mudge, J. Mars, and L. Tang,
“Neurosurgeon: Collaborative intelligence between the cloud and mobile edge,”
in Proceedings of the Twenty-Second International Conference on Architectural Support
for Programming Languages and Operating Systems. ACM, 2017, pp. 615–629.

Tools

* [VLFeat](http://www.vlfeat.org/api/index.html).
Portable C library with lots of feature extractors for computer vision tasks.

### Segmentation

[ENet: A Deep Neural Network Architecture for Real-Time Semantic Segmentation](https://towardsdatascience.com/enet-a-deep-neural-architecture-for-real-time-semantic-segmentation-2baa59cf97e9)
0.7 MB weights (16 bit floats). 3.83 GFLOPS on 3x640x260 images.


### Classifying JPEG-compressed data

Can one do classification and object detection on compressed JPEG straight from the camera?
Instead of computing the framebuffer from the JPEG.

Can it be also done in a streaming fashion?

Operating on the blocks with DCT coefficients.

Prior work:

- [Faster Neural Networks Straight from JPEG](https://openreview.net/forum?id=S1ry6Y1vG).
ICL2018. Modified libjpeg to return DCT coefficients. Blocks of 8x8. On ResNet50, 1.77x faster, same accuracy.
- [On using CNN with DCT based Image Data](https://www.scss.tcd.ie/Rozenn.Dahyot/pdf/IMVIP2017_MatejUlicny.pdf). IMVIP 2017.

References

* [JPEG DCT, Discrete Cosine Transform (JPEG Pt2)- Computerphile](https://www.youtube.com/watch?v=Q2aEzeMDHMA).
Excellent visual walkthrough of JPEG compression and decompression. CbCrY,DCT,quantization,Huffman encoding. 


## New sensor types

[How ML/DL is Disrupting Sensor Design](https://drive.google.com/file/d/0BzrlDxVZWSUpbkZrRnlMbmE2c2s/view).
Compressed sensing. Random projections.

[Rise of the super sensor](https://www.computerworld.com/article/3197685/internet-of-things/google-a-i-and-the-rise-of-the-super-sensor.html).
CMU has developed a generic 'synthetic sensor', using audio/vibration etc.
"the revolution is to install a super sensor once, then all future sensing (and the actions based on that sensing)
is a software solution that does not involve new devices"

Soft Robotics
[Youtube video about easy-to-construct soft gripper with integrated resistive sensors](https://www.youtube.com/watch?v=BLE5yhS3k3I).
Could train algorithms to detect objects gripped.

## Time series

Deep learning for time series classification: a review. https://arxiv.org/abs/1809.04356
Compares many different model types across 97 time-series datasets.
Finds that CNNs and ResNet performs the best.


## Change detection

Novelity detection.
Anomaly detection.

Change point detection.
In Time series, at which point something changes.
Often growth rate. Can also be amplitude.
Changes in distribution.

Breakout detection.
In time series, when the mean shifts relatively suddenly.
Mean divergence/shift. Or transition too/from (rampup).

Usecases

* Network Intrusion Detection (IDS)
* Condition Monitoring of machines

Resources

* [Change point detection in time series data with random forests](https://www.sciencedirect.com/science/article/pii/S0967066110001073)
* [Two approaches for novelty detection using random forest](https://www.sciencedirect.com/science/article/pii/S0957417414008070)
* [Introduction to Anomaly Detection: Concepts and Techniques](https://iwringer.wordpress.com/2015/11/17/anomaly-detection-concepts-and-techniques/). Very good overview, with recommendations for different cases
* [Awesome Time Seeries Anomaly Detection](https://github.com/rob-med/awesome-TS-anomaly-detection).
Lists software packages and a few labling tools and benchmark datasets.
* [Twitter: Introducing practical and robust anomaly detection in a time series](https://blog.twitter.com/engineering/en_us/a/2015/introducing-practical-and-robust-anomaly-detection-in-a-time-series.html).
* [](https://anomaly.io/anomaly-detection-using-twitter-breakout/).
Based on Mean Shift Clustering.
Based on algorithm called E-Divisive.
E-Divisive with Medians (EDM) faster version, estimates median using interval trees. 
Mentions Moving Median as a statistic which is robust to anomalies.
* [Anomaly detection and condition monitoring](https://towardsdatascience.com/how-to-use-machine-learning-for-anomaly-detection-and-condition-monitoring-6742f82900d7).
PCA for dimensionalty reduction, and using Mahalanobis distance (MD) threshold for anomaly detection.
AutoEncoder as alternative. Learned dimensionality reduction, using probability distribution of recontruction error for anomaly detect.
Demonstrated on NASA Gear Bearing failure example.
By Axibit AS.
* [Anomaly detection strategies for IoT sensors](https://medium.com/analytics-vidhya/anomaly-detection-strategies-for-iot-sensors-6281e84263df)
Point-wise anomalies: individual devices.
Collective anomalies: multiple devices together.
Contextual anomalies: takes into account context, such as day-of-week etc.

Software

* [tslearn](https://github.com/rtavenar/tslearn).
Time-series machine learning tools. scikit-learn inspired
* [seglearn](https://github.com/dmbee/seglearn)
Time-series. scikit-learn inspired.
* [banpei](https://github.com/tsurubee/banpei).
Change-point detection using Singular Spectrum Transform (SST),
Outlier detection using Hotelling's theory.


Datasets

* [Outlier Detection DataSets (ODDS)](http://odds.cs.stonybrook.edu/).
Huge number of datasets.
In multiple groups:
Multi-dimensional point,
time-series point (uni/multivariate),
time-series graph data,
adverserial/attack data,
* Numenta Anomaly Benchmark [NAB](https://github.com/numenta/NAB).
50+ different time-series, benchmarked on many methods.
* [UCSD Anomaly Detection Dataset](http://svcl.ucsd.edu/projects/anomaly/dataset.htm).
Video of pedestrian walkway. Anomalies are non-pedestrians.
A subset has pixel-level masks. 

Methods

* [DeepADoTS](https://github.com/KDD-OpenSource/DeepADoTS).
From paper "A Systematic Evaluation of Deep Anomaly Detection Methods for Time Series". 
Implements 7 deep neural models for anomaly detection.
* [telemanom](https://github.com/khundman/telemanom).
STMs to detect anomalies in multivariate time series data.
Includes anomaly dataset from NASA Mars Rover.


# Online learning

It is also desirable to learn on-the-fly.
First level is hybrid systems where new samples is used to tune/improve a pre-trained model.
More advanced is on-line training which can automatically detect new classes.
Get closer to typical Artificial Intelligence field, since now have an intelligent agent able to learn on its own.

Hybrid learning, adaptive machine learning, progressive learning, semi-supervised learning.
Q-learning (reinforcement learning).

# Transfer learning
...

## Sparsity

[Sparsity Lesson of Fundamentals of Digital Image and Video Processing](https://www.coursera.org/lecture/digital/applications-MNbjB)
Applications. Noise smoothing, inpainting, superresolution. Foreground/background separation. Compressive sensing.
Images are sparse in DCT decomposition. Can throw away many of the with minimal quality loss.
Noise is not correlated and will not compress well. This fact used in image denoising.
Compute a sparse representation, then reconstruct. Can be done with standard basis like DCT, or a learned dictionary.
Basis pursuit. Matching Pursuit. Orthonogonal Matching Pursuit. 
Foreground/background separation in video. Singular Value Decomposition. 
Can one do foreground separation of audio in a similar manner?

Compressive Data Aquisition. Replace sampling at Nyquist followed by compression with.
Sampling matrices. Suprising result: Random matrices work.


