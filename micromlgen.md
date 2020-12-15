# micromlgen

https://github.com/eloquentarduino/micromlgen
supports SVM

blogpost announcement references emlearn
cites missing SVM as a limitation
https://eloquentarduino.github.io/2019/11/you-can-run-machine-learning-on-arduino/

got some tutorial here
using SVM for gesture recognition
https://eloquentarduino.github.io/2019/12/how-to-do-gesture-identification-on-arduino/

## Relevance Vector Machine.
https://en.wikipedia.org/wiki/Relevance_vector_machine
Was patented by Microsoft. Lapsed in 2019?
https://eloquentarduino.github.io/2020/02/even-smaller-machine-learning-models-for-your-mcu/
tries to be more sparse than SVM
can output probablities

## SERF
https://eloquentarduino.github.io/2020/07/sefr-a-fast-linear-time-classifier-for-ultra-low-power-devices/
based on paper

### SEFR: A Fast Linear-Time Classifier for Ultra-Low Power Devices
8 Jun 2020
https://arxiv.org/abs/2006.04620
Linear time complexity. Like Naive Bayes
SEFR outperforms Naive Bayes on 3 out of 5 datasets
Did not try PCA before Naive Bayes though.

Training 100 samples with 100 features in 200 ms on an Arduino Uno
