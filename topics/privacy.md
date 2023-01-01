
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

