
Many deployment scenarios for TinyML systems can be exposed to a very diverse set of input data.
Including data that might not be in the classes-of-interest, or in the initial dataset at all.
This can pose a challenge for Machine Learning based classifiers,
because they tend to perform very poorly on out-of-distribuion data.

#### Question
One question from the Sound of AI community.

> I am trying to create a deep learning model to classify five different bird calls:
> Brown-Tinamou, Cinereous-Tinamou, Great-Tinamou, Little-Tinamou, and Small-billed-Tinamou.
> I have built a Convolutional Neural Network (CNN) model to perform this classification, and the training and validation accuracies are around 90%.
> However, I am encountering an issue. When I use the model to predict bird calls from a different species that were not included in my training data,
> the model still tries to classify these new bird calls as one of the five classes, resulting in false positives.
> I need advice on how to prevent the model from falsely classifying bird calls that do not belong to any of the training classes.

#### Answer

This is expected behavior - a classification model will (in itself) only behave well on data it has been trained on.
Anything outside that, and the model will be "confidently wrong".
This can even happen for silence, white noise, speech etc.

One common approach is to add an "other" / "unknown" class. This must then contain samples from all the other possible sounds (that the model is likely to encounter when deployed). It would include other birds, maybe speech, silence et.c. Generic open datasets such as AudioSet (from Youtube) can be useful here. But ideally it would be recorded in the same way the data you have for sounds-of-interest (the mentioned birds).

Another approach is to use outlier detection. Which is trained on your in-distribution data, and will cause high outlier scores for anything different from this.
If you have a CNN, then using the layer where all features have been merged - just before the classification layer(s) is a good candidate for the data for this model. You can use a reconstructing autoencoder with fully-connected-layers, or a traditional model such as a Gaussian Mixture Model.
This can be used instead of, or in combination with the above unknown-class approach.
In either case, it is wise to include out-of-distribution samples in your evaluation for the system - so that you can measure how well your model does on this out-of-distribution samples.
