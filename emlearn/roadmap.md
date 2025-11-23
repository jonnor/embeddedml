
# Roadmap

Strategy. Keeping things application-oriented.
Making sure that it is easy to achieve practical tasks,
and that this documented well, and the utility is well demonstrated.

## Next

Support for the standard tasks,
classification, regression and outlier/anomaly detection.

Demos

- Complete IMU classification example in C
Including pre-processing / feature extraction, training pipeline, on-device checks from dataset
HAR in emlearn-micropython is a good starting point
Walking detection, ref https://www.nature.com/articles/s41746-022-00745-z ?

Data loading

- Support Numpy .npy files

Classifiers

- Output an enum with the class information, and a const char array
- Switch to only output one inference method at a time.
- Add a wrapper function also in the loadable case, for uniform C API

Documentation

- 

## Preprocessing improvement

Preprocessing

- Feature scaling. StandardScaler/MinMax/RobustScaler
- Feature transformations. Support custom C code

Documentation

- Update feature extraction section

Examples

- Example of custom feature transformation/extraction

## Benchmarking

Documentation

- Benchmark common targets.
Illustrate model size "boundaries", for different microcontrollers.
Measure execution time for trees. Compare with the compute size estimates

Examples

- Add KNN to classifiers example. Need to setup distance working buffer for _predict


## Event Detection

Models

- knn. Support proba

Preprocessing

- SignalWindower

Examples

- PR curves / threshold tuning
- SignalWindower. Time-based features.
- Signal. LAF soundlevel. Using IIR filters

Demos

- ? Heartrate detector
- Impulse sound detector
- Voice Activity Detection (VAD) - energy based

## Optimized trees

Work ongoing for a leaf quantization/clustering paper.
github.com/jonnor/leaf-clustering/

Benchmarking

- Comparison with m2cgen and micromlgen
- Comparison with neural networks (MLP)
Compare program memory size and execution time, vs performance.
Need hyperparameter optimization to find good cost/performance tradeoff.
tflite micro (int8), vs emlearn MLP (float)

Marketing

- Write a blogpost 
- Make a 2 minute video summary

Outreach

- Notify existing users of the optimized models trees.
https://www.informatica.vu.lt/journal/INFORMATICA/article/1281/text


## Zephyr support

Platform support

- Use Zephyr QEMU to run tests in CI

Demos

- Motion classification.
Toothbrush / walking model. On XIAO etc


## Sound Event Detection

Preprocessing

- Mel-spectrogram. Using SignalWindower? Or dedicated code
- Maybe also MFCC/DCT
- Sound Event Embedding vectors. Using pretrained CNN. On AudioSet strong? CRNN pretrainer. 

Models

- GRU recurrent neural network. Keras import

Demos

- Custom Sound Event Detection.
Car passing? Environmental Sounds?
- Voice Activity Detection
- Speech Commands / keyword spotting
- Few-shot SED using embeddings + KNN

## Misc

Start writing a CHANGELOG.md
- or add it to docs like sklearn/skimage/librosa etc.?


## 1.0 - complete broad support

Support the full width of common models.

Models

- net. MLP autoencoder for anomaly/outlier
- linear. Linear regression. Move from emlearn-micropython
- linear. Logistic regression
- neighbour. kNN regression
- neighbour. Nearest centroid 
- neighbour. Outlier/anomaly
- kernel. SVM regression
- kernel. SVM classification
- kernel. One-class SVM
- trees. IsolationForest inference


### Support Vector Machine

People online interested in it for microcontrollers

* https://stackoverflow.com/questions/8360253/how-to-extract-info-from-scikits-learn-classifier-to-then-use-in-c-code
* https://stackoverflow.com/questions/48912695/how-to-extract-learned-ml-model-for-distinct-implementation
* https://forum.arduino.cc/t/need-help-support-vector-machine-for-esp32-arduino/1022594

### Logistic regression

Preferably implemented with integer only math
Easy apart from the sigmoid and softmax functions


Someone that asks for it
https://stackoverflow.com/questions/46438860/would-i-be-able-to-compile-external-libraries-opencv-mlpack-onto-an-mcu/46441692#46441692

Someone looking for PCA
https://stackoverflow.com/questions/70251197/how-do-i-store-a-fitted-pca-so-that-i-may-transpose-unseen-testing-dataset-i-do



# emlearn-micropython roadmaps 

### Audio TinyML

Levels

- SoundLevelMeter. DONE
- SpectrumAnalyzer
- Speech Commands. CNN. Google dataset
- Voice Activity Detection. CNN/RNN/CRNN
- Applause Detection
- Sound Event Detection. CRNN. ? Which stock task/dataset
- Generic AudioClassifier. AudioSet

Hardware enablement

- PDM ESP32 microphone support
- Unix microphone support

Tooling

- Read/write .wav files. A wavfile module
- Data recording. .wav files on disk, .wav send to server
- Data labeling. LabelStudio integration?

Preprocessing

- FFT. DONE
- Soundlevel. DONE
- Spectrogram

Collaboration

- ?


## IMU TinyML

Levels

- Human Activity Detection
- Gesture Detection

Preprocessing

- Spectral. Using FFT
- Interval trees? quant etc
- Gravity removal. Low-pass

Collaboration possibilities

- Smartwatch projects? https://github.com/wasp-os/wasp-os



### Softmax

CMSIS-NN uses a softmax with base 2 instead of base e
Has q15 and q7 versions available
https://www.keil.com/pack/doc/CMSIS/NN/html/group__Softmax.html#ga1cacd8b84b8363079311987d0016ebe5

? is this compatible with sklearn ? or keras Softmax

tflite micro
https://github.com/tensorflow/tflite-micro/blob/6d337dc9f96a7f01ac90f3bf8363828fbdfe1e3a/tensorflow/lite/kernels/internal/reference/softmax.h#L68

Various exp optimizations
https://github.com/mratsim/laser/blob/master/research/exp_and_log_optimisation_resources.md

https://github.com/asmekal/softmax-acceleration/blob/master/Fast%20softmax%20approximations.ipynb

### Sigmoid

Typical definition uses expf, which is slow

There are alternative functions that are much faster
https://stackoverflow.com/questions/10732027/fast-sigmoid-algorithm/15703984#15703984

CMSIS-NN uses a lookup table
https://arm-software.github.io/CMSIS_5/NN/html/group__Acti.html#ga8932b57c8d0ee757511af2d40dcc11e7
Either 256 entries for q7 (256 bytes),
or 128+192 for q15 (640 bytes)

Q7 approach seems suitable for emlearn

## 2.0 - on-device learning

Models

- Isolation Forest training. In C. For continious AD/novelty detection
- Random Forest training. In MicroPython ?
- Maybe move addnode/addroot from emlearn-micropython to emlearn

Demos

- Anomaly Detection in rotating machine. Using accelerometer or sound

## Later

- Streaming stats/summaries
- DTW / on-device gesture detection etc


# numpy .npy support

### .npy file support in C

#### onai/npio

https://github.com/onai/npio

- MIT licensed
- Has proper Python dict parser, and dtype parser
- Uses file descriptor ints as interface
- Allocates internally

#### npy_array
https://github.com/oysteijo/npy_array

- Seems to work without seek
- Quite simple header parsing
- Uses FILE API
- Supports npz via libzip
- Supports mmap for read
- Simple usage examples
- Provides variadic macros for constructing shape and array info
- No support for streaming write?

#### elgw/npio
https://github.com/elgw/npio

- MIT
- Allocates internally
- Uses FILE interface
- No support for streaming?

#### micropython-ulab
https://github.com/v923z/micropython-ulab/blob/825ec2b143ebd8d3d3707bac2af0fe1ae6cb401a/code/numpy/io/io.c#L53

- Implements numpy .npy files in io_load and io_save
- Designed for microcontrollers
- Uses memcpy to build up the header, not string formatting
- Has a minimal sprintf for size_t
- Also implements number parsing manually
- Reads a fixed 128 bytes for header. Then seeks to data start

#### C++

https://github.com/fengwang/cnpypp
https://github.com/cdcseacave/TinyNPY
https://github.com/rogersce/cnpy
https://github.com/llohse/libnpy

