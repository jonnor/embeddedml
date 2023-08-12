
# Roadmap

Strategy. Keeping things application-oriented.
Making sure that it is easy to achieve practical tasks,
and that this documented well, and the utility is well demonstrated.

## Next

Support for the standard tasks,
classification, regression and outlier/anomaly detection.

Examples

- Add KNN to classifiers. Need to setup distance working buffer for _predict

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

Tools

- Size measurement support, via ELF

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

- trees. Use int16_t features and integer-only math. Switch to 8 byte nodes (from 12).
- preprocess. Float to int16 quantizer
- trees. Switch to 4-byte nodes. Implicit left, 8 bit relative jump. Ref feedback from Martin
- trees. Runable leaf-node quantization / de-duplication
- bfloat16 support for regression?

Examples

- Inline vs loadable codegen for trees. Mention in documentation

Benchmarking

- Comparison of emlearn 0.15.x trees vs NEW trees. Size and inference time
- Comparison with m2cgen and micromlgen
- Tool for measuring RAM and FLASH memory

Outreach

- Notify existing users of the optimized models trees.
https://www.informatica.vu.lt/journal/INFORMATICA/article/1281/text


## Zephyr support

Platform support

- Create a Zephyr module
- Get Zephyr QEMU simulator to work
- Use Zephyr QEMU to run tests in CI

Demos

- Something on RuuviTag?


## Sound Event Detection

Preprocessing

- Mel-spectrogram. Using SignalWindower? Or dedicated code
- Maybe also MFCC/DCT
- Sound Event Embedding vectors. Using pretrained convolutional 

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



