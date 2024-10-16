
# Roadmap

Strategy. Keeping things application-oriented.
Making sure that it is easy to achieve practical tasks,
and that this documented well, and the utility is well demonstrated.

## Next

Support for the standard tasks,
classification, regression and outlier/anomaly detection.

Examples

- Add KNN to classifiers example. Need to setup distance working buffer for _predict

Demos

- Color detector. In C/Arduino
- Color detector online learning. In MicroPython ?


## Preprocessing improvement

Preprocessing

- Feature scaling. StandardScaler/MinMax/RobustScaler
- Feature transformations. Support custom C code

Documentaion

- Update feature extraction section

Examples

- Example of custom feature transformation/extraction

## Benchmarking

Documentation

- Benchmark common targets.
Illustrate model size "boundaries", for different microcontrollers


## Event Detection

Models

- trees. Support proba
- knn. Support proba

Preprocessing

- SignalWindower

Documentation

- Small reference for each model family.

Examples

- PR curves / threshold tuning
- SignalWindower. Time-based features.
- Signal. LAF soundlevel. Using IIR filters

Demos

- ? Heartrate detector
- Impulse sound detector

## Optimized trees

Models

- trees. Runable leaf-node quantization / de-duplication
- trees. Switch to 4-byte nodes. Implicit left, 8 bit relative jump. Ref feedback from Martin
- trees. bfloat16 or Q/int16 support for regression?

Examples

- Inline vs loadable codegen for trees. Mention in documentation

Benchmarking

- Comparison of emlearn 0.15.x trees vs NEW trees. Size and inference time
- Comparison with m2cgen and micromlgen
- Tool for measuring RAM and FLASH memory

Documentation

- Make a paper to go on Arxiv. Consider submitting to conferences/journals

Marketing

- Write a blogpost Medium 
- Make a 2 minute video summary

Outreach

- Notify existing users of the optimized models trees.
https://www.informatica.vu.lt/journal/INFORMATICA/article/1281/text


## Zephyr support

Platform support

- Use Zephyr QEMU to run tests in CI

Demos

- Something on RuuviTag?


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
- linear. Linear regression
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


### Softmx

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
- DTW / Gesture detection



