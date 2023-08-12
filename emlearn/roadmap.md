
# Roadmap

Strategy. Keeping things application-oriented.
Making sure that it is easy to achieve practical tasks,
and that this documented well, and the utility is well demonstrated.

## Next

Support for the standard tasks,
classification, regression and outlier/anomaly detection.

Examples

- Add KNN to classifier comparison. Need to setup distance working buffer

Demos

- Color detector. In C/Arduino
- Color detector online learning. In MicroPython ?


## Misc

- Feature scaling.
- Feature transformations. Support custom C code

## Event Detection

Models

- Support proba with trees

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

## 1.2 - optimized models

Fixed-point support for primary models.

- trees. Use int16_t features and integer-only math.
- preprocess. Float to int16 quantizer
- trees. Optimized RF inference

Benchmarking

- Tool for measuring RAM and FLASH memory

## Sound Event Detection

Preprocessing

- Mel-spectrogram. Using SignalWindower

Models

- GRU recurrent neural network. Keras import

Demos

- Sound Event Detection.
Car passing? Environmental Sounds?
- Voice Activity Detection
- Speech Commands / keyword spotting

## 1.0 - complete broad support

Support the full width of common models.

Models

- net. MLP autoencoder
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

? micropython
- Isolation Forest
- Random Forest

## Later

- Streaming stats/summaries
- DTW / Gesture detection


