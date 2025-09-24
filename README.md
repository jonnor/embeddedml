# Machine learning on embedded devices

Focused primarily on running inference/prediction/feed-forward part on a microcontroller (or small embedded device).
Training phase can run on a standard computer/server, using existing tools as much as possible.

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
Audio, video.
* Unreliable connection
* High bandwidth sensor input.
Audio, video, accelerometer/IMU, current sensor, radiowaves.
* Low bandwidth algorithm output
* Events of interest are rare
* Low energy usage needed
* Full/raw sensor data is not valuable to store
* Sensor system should be low cost

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

More notes on [Applications](./applications)

### Motivation

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
* [How to run deep learning model on microcontroller with CMSIS-NN](https://www.dlology.com/blog/how-to-run-deep-learning-model-on-microcontroller-with-cmsis-nn/).
Why run deep learning model on a microcontroller?
Sensitive data gets to the cloud, photos, and audio recordings.
The company who sells this may charge a service fee to use its service and even worse sell your private data.
It won't work without the network connection to the server.
Data traveling back and forth between the device and server introduces lag.
Require network and wireless hardware components on the circuit design which increase the cost.
It might waste bandwidth sending useless data.


## State of the Art in 2019
Of ML inference on general-purpose microcontrollers.

```
TODO: update for 2023
```

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


# Own contributions

Presentations

- [Sensor data processing on microcontrollers with MicroPython and emlearn](./presentations/PyConZA2024/) - October 2024
- [6 years of open source TinyML with emlearn](./presentations/TinymlEMEA2024) - June 2024
- [emlearn - Machine Learning for Tiny Embedded Systems](./presentations/EmbeddedOnlineConference2024) - May 2024
- [Machine Learning on microcontrollers using MicroPython and emlearn](./presentations/PyDataBerlin2024/). PyDataBerlin & PyCon DE - April 2024 

Open source software projects

- [emlearn](https://github.com/emlearn/emlearn). Machine Learning inference engine for Microcontrollers and Embedded devices.
- [emlearn-micropython](https://github.com/emlearn/emlearn-micropython). Efficient Machine Learning engine for MicroPython.


# Learning material

Books

* [Learning in Embedded Systems](https://mitpress.mit.edu/books/learning-embedded-systems), May 1993.
* [TinyML: Machine Learning with TensorFlow on Arduino, and Ultra-Low Power Micro-Controllers](https://tinymlbook.com/). January, 2020.
* [TinyML Cookbook](https://www.packtpub.com/product/tinyml-cookbook/9781801814973)

Articles

- [Embedded.com: Applying machine learning in embedded systems](https://www.embedded.com/applying-machine-learning-in-embedded-systems)
- [Embedded.com: Transfer learning for the IoT](https://www.embedded.com/transfer-learning-for-the-iot/)

# Tools

Open-source

* [emlearn](http://github.com/emlearn/emlearn). Inference engine for microcontrollers.
Supports converting scikit-learn models to plain C code.
No dynamic allocations. No runtime needed.
* [TensorFlow Lite for Microcontrollers](https://www.tensorflow.org/lite/microcontrollers).
Supports neural network models made with TensorFlow (including Keras).
Can run on wide range of platforms.
Since November 2018. Supports ARM Cortex M, RISC-V, ESP32/Xtensa and Linux/MacOS host.
Requires a runtime, aroud 20 kB.
* [onnx2c](https://github.com/kraiskil/onnx2c). Allows generating C code from ONNX models.
* [iree](https://iree.dev/guides/deployment-configurations/bare-metal/). Compiler. Around 30 kB runtime.
* [executorch](https://github.com/pytorch/executorch). C++ framework for deploying PyTorch models.
Around 50 kB runtime. Supports bare-metal via "Portable" operations, or specialized for Cortex M.
* [nnom](https://github.com/majianjia/nnom) - Fixed-point neural network compiler for microcontrollers.
Supports wide range of networks. Outputs plain C code. Can use CMSIS-NN on ARM Cortex M.
- [micromlgen](https://github.com/eloquentarduino/micromlgen)
* [Embedded Learning Library](https://github.com/Microsoft/ELL) by Microsoft.
Set of C++ libraries for machine learning on embedded platforms. Includes code for kNN, RandomForest etc.
Also has some node-based dataflow system in place it seems. JavaScript and Python bindings.
* ONNC project has a [backend for ARM Cortex M](https://github.com/ONNC/onnc-tutorial/blob/master/lab_2_Digit_Recognition_with_ARM_CortexM/lab_2.md) (using CMSIS-NN)
and a [C backend](https://github.com/ONNC/onnc/blob/74e59908b2881844329c3d330eea7a7c306e1e22/docs/ONNC-C-Backend-Guide.md).
Allows to convert an ONNX models to run on devices.
- [nn4mc_cpp](https://github.com/correlllab/nn4mc_cpp).
Neural Networks for Microcontrollers.
Supports Keras natively. Provides instructions for PyTorch et.c via ONNX.
Documentation for using from Python is lacking, as well as the type of networks supported.
Does not seem maintained since 2020.
* [uTensor](https://github.com/uTensor/uTensor).
Export Tensorflow model to mbed/ARM microcontrollers.
Not supported on ESP32 or RISC-V or similar.
* [Embedded Classification Software Toolbox](https://github.com/ma2th/ecst).
Unmaintained since 2018.
- [sklearn-porter](https://github.com/nok/sklearn-porter).
Can compile DecisionTreeClassifier and SVC models to C.
Uses dynamic memory.
Not optimized for use on embedded devices.
* [microTVM](https://tvm.apache.org/docs/topic/microtvm/index.html).
Depends only on the C standard library, and runs bare metal such as STM32 and NRF52 microcontrollers.
Is under development. Which models are supported on microcontrollers not specified.

Proprietary

* X-CUBE-AI for STM32


# Models

A range of Machine Learning models are useful in an embedded devices setting.
Classical methods are used when the amount of data is quite small,
and neural networks for large datasets and complex inputs.

Below are notes on the various models in the context of embedded Machine Learning,
including model size and compute-time optimization.

- [Tree-based methods](./models/tree-based.md).
Random Forest, Extratrees, Decision Trees, et.c.
- [Neural Networks](./models/neural-networks.md).
Convolutional Neural Networks (CNN), Recurrent Neural Networks (RNN), Autoencoders
- [Support Vector Machines](./models/support-vector-machine.md) (SVM).
- [Mixture models](./models/mixtures.md).
Gaussian Mixture Models (GMM).
- [Nearest Neighbours](./models/k-nearest-neighbours.md). kNN et.c.


# More topics

- [Privacy](./topics/privacy.md)
- [Energy usage](./topics/energy-usage.md)
- [Model size](./topics/model-size.md)
- [On-device learning](./on-device-learning)




