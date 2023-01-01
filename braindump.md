
# MATLAB, Sensor Data Analytics

MATLAB. [Signal Processing and Machine Learning Techniques for Sensor Data Analytics](https://www.youtube.com/watch?v=GZ3KUPqA1JM).
Accelerometer data. Human Activity Recognition.
Nice visualization of the 3-axis plus label and prediction data.
As fast-forward animation. Time-scope allows markers and triggers.
Extracts 64 features. mean,rms,highpass-peaks,autocorrelation.
Nice app for filter design. Fields for relevant, explanation graph, plots for checking results. 
Nice app for classification selection. 
Also has Neural Network toolbox.
MATLAB integrated support for Android and iOS devices.
Code generation of NN using `genFunction`. And then translate to C using `codegen`.
Highlights differences between offline and real-time processing.
Has a stream/step interace for real-time.

Other applications

- Mobile sensing
- Structural Health Monitoring
- Fault and event detection


## [Designing data pipelines for analytics and machine learning in industrial settings(https://www.youtube.com/watch?v=rraNNlr3evM).
IIoT data pipelines.
Ingest. Persist. Analyze.


## Machine Learning Logistics
https://www.oreilly.com/library/view/machine-learning-logistics/9781491997628/
Free ebook.
Ted Dunning (MapR founder).

Highlights online/production comparison of
new versus old models. Incumbent and challenger.

Recommends 'Rendevouz' architecture for putting models into production
https://mapr.com/ebooks/machine-learning-logistics/ch03.html
Decouple request, put into a message queue.
Run multiple models in parallel. Eg new model and old model, plus
a basic 'canary' baseline model to detects shifts in data.
Explains useful metrics a bit. Latency tracing.
Recommends automated analytics on logs/metrics,
ex anomaly detection on processing latency.
call this 'Meta Analytics'

https://mapr.com/ebooks/machine-learning-logistics/ch07.html#meta_analytics
Event Rate Change Detection
Recommends log-scale for histograms, to make anomalous tails easier to see.
Mentiods use of tracing-metrics, to analyze where/which step is taking long.
Recommends setting a budget for troubleshooting (in hours / per week)
- this is used to set thresholds for anomaly detections.
Half of this budget will be for (inevitable) false alarms.
Should have a prioritation scheme.
Suggests normalizing monitoring signals to.
Adding together all signals to single signal by adding as log-odds


T-digest. 
https://github.com/tdunning/t-digest
Streaming estimation of quantilies
Improvement over Q-digest .
? 5000 lines of Java...

Python implementation in some hundred lines
https://github.com/CamDavidsonPilon/tdigest


Practical Machine Learning: A New Look at Anomaly Detection
https://mapr.com/practical-machine-learning-new-look-anomaly-detection/
Ted Dunning and Ellen Friedman


## A review on TinyML: State-of-the-art and prospects
https://www.sciencedirect.com/science/article/pii/S1319157821003335

