
# On-device learning


## See also

- activity-detection.md
- roadmap.md

## Suitable models/methods

- Extratrees
- KNN
- Logistic Regression
- Linear Regression
- PLSR

## Teachable Machine

A "teachable machine" with MicroPython ?
For example for image classification. Using a pretrained MobileNet.
And then KNN and/or logreg on top.
Web interface for labeling the data, and triggering the learning process.
MicroDot as framework
Should store JPEG images to SDcard.
Also store image vectors? Maybe also basic features. Ex brightness, normalized histograms
Would want to do change detection over time. Mostly store interesting things
Would want to store data structured by time. Ex: year/month/day/hour/minute
! this is 0.5 million folders per year.
8600 hours. Seems more reasonable. Would need stress testing
ESP32-cam has SDcard slot
! T-Camera does not have SDcard support..
Might want to do a PCA projection from MobileNet down to something smaller

