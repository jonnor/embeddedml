
# TODO

- Fix emlearn pip install in jupyter-lite.
Need a pure Python wheel. Get rid of last extensions.
- Import some motion / HAR type datasets, store on device
- Test transferring the data from device using MicroDot


# Planning

## Takeaways

- MicroPython enables physical computing for those that know Python
- Applicable to many data-oriented applications. Especially those incorporating sensors
- MicroPython enables scaling down to hardware that costs 10 USD
- emlearn-micropython enables running machine learning classifiers 
- Can also run in the browser. Interactive, data visualization, etc
- MicroPython in browser enables much faster loading compared to big Python
- asyncio enables concurrency



## Structure

What was promised

- Measuring the surroundings using sensors
- Connectivity using WiFi
WiFi credential management
- Data storage using on-board filesystem
Time-series storage
- Serving a webui for configuration/control, using Microdot
API to download data
- Automated data processing/analysis using DSP and ML, with emlearn-micropython
Known feature extraction
FFT analysis.
Histogram analysis.
Motion classifier using Random Forest
Pretrained models?
- Enabling interactive data analysis via webui
Browsing timeseries. Selecting sections, comparing. Using Plotly?
Search for motifs? Repeating occurrences
Search for anomalies?

- Managing concurrency on microcontroller, using asyncio
- Optional integration. Pull using HTTP, and/or push using Webhooks/MQTT

Nice to have:

- Event log. That can be accessed via. Both for internal
- Discovery device of using mDNS
- Labeling. Coarse labels in time. And find-grained labeling - events.

# Notes


## Ideas

Concepts

- Serve MicroPython WASM from device. To do learning in browser. Send model back?
- Doing data labeling in browser
- Doing data curation/cleaning in browser
- Doing training in browser

Usecases

- Lab gear. For scientific/engineering uses
- Wireless Sensor Networks. Ref EuroScipy Krakow 2025
- Educational lab exercises.
- Robotics.
- DIY/Maker/kits. For niche cases. Or open-ended.

Demos

- Motion classification
- Audio analysis / Sound Event Detection
- UV-Vis-NIR spectroscopy
- Gesture recognition. With built-in learning. Datavis in browser
- Indoor localization and mapping

Random

- Reference Amy, and their in browser ?

Things I am intereted in

- Time series compression
- Reservoir sampling
- Continual online learning
- Anomaly detection
- Adaptive sampling
- Adaptive data thinning

## MicroPython and emlearn in browser

- Make a browser demo for inference. Basically same kind of model as on device.
- Browser demo, heavier model, running on instances on-device model flagged of interest
- Make a brower demo for labeling
- Make a browser demo of training
- Make a browser demo for train-in-browser + deploy-on-device




## Plotting libraries

https://community.plotly.com/t/how-can-i-reduce-bundle-size-of-plotly-js-in-react-app/89910/2
plotly.js cartesian should be enough
Minified gzipped is 420.3 kB

## Storage

8 MB FLASH total

- MicroPython ESP32 2 MB with .py/.mpy libraries
- Web assets. Incl Plotly, MicroPython.wasm. 2 MB 
- Data storage internal. 4 MB

0.125 ms soundlevels - 4 bytes per entry. 
*8*60*60*24 / 1e6 = 2.76 MB per day

1 minute soundlevels, 3 metrics, 4 bytes each.
3*4*60*24*30 / 1e6 = 0.5184 MB per 30 days

50 Hz accelerometer data - 6 bytes for 3 channels.
3*2*50*3600*23 / 1e6 = 24.84 MB per 24 hours
Want to compress by a factor of 10x. Sounds doable.

Effects of Sampling Frequency on Human Activity Recognition with Machine Learning Aiming at Clinical Applications
https://pmc.ncbi.nlm.nih.gov/articles/PMC12196717/
Reducing the sampling frequency to 10 Hz did not significantly affect the recognition accuracy for either location. 

20-25 Hz would be sufficient.

! would want gyro data also.
Or orientation and linear acceleration separated out.
! requires deciding the gyro mixing ratio

## Datasets

PAMAP2 original

  197.7 MiB [###########################]  subject102.dat
  181.2 MiB [########################   ]  subject108.dat
  165.7 MiB [######################     ]  subject105.dat
  160.5 MiB [#####################      ]  subject106.dat
  146.1 MiB [###################        ]  subject104.dat
  139.1 MiB [##################         ]  subject107.dat
  135.1 MiB [##################         ]  subject101.dat
  112.4 MiB [###############            ]  subject103.dat
    3.7 MiB [                           ]  subject109.dat

1.3G	/data/emlearn/PAMAP2_Dataset/Protocol/

PAMAP2 Parquet default settings

  749.1 MiB [###########################]  pamap2.parquet

Total time around 8 hours, approx 1 hour per subject.
Multiple IMUs, 100 Hz.

Getting 6 axis from hand IMU, with int16, storing as delta-encoded Parquet (no index).
5.2 MB per 8 hours, or 0.65 MB per hour

8 * 5.349397e6 / (574306*6), 'bits per sample'
(12.41938850252885, 'bits per sample')

! not that much compression, considering native is 16 bits
Was hoping for 4x compression at least, 4 bits effective

Would probably need to
1) quantize smaller values - likely to be noise anyway
2) estimate orientation and linear acceleration. Ex using complimentary filter

Try blosc2 with HDF5 as alternative.

Try StreamVByte or Simple8B/Simple9/Simple16

Brainstorming
https://claude.ai/chat/f0c3b34d-9e4b-4121-8f16-b2c3f63aecbc

## Hardware platform

- M5Stick C PLUS 2. ! PDM mic, not I2S. 8 M FLASH / 2 MB PSRAM
- Lilygo T-Watch ESP32 S3 watch
- T-Camera V3 2020. ! obsolete
- T-Camera S3. Missing PMU code. 16MB FLASH / 8 MB PSRAM
- XIAO ESP32S3 Sense. Includes SDcard. ! PDM mic, not I2S

https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/

## What are the limitations?

How fast/much data can one serve over HTTP (from RAM and from disk)?
Target response time for loading data: Under 1000 ms

Avoiding transformation.
But using chunking/partitioning


## Can time-series compression help data storage and transfer limitations?

Can we get interesting data storage for IMU data for multi-day into 4 MB?

! 



## jupyter-lite for scikit-learn

https://scikit-learn.org/stable/lite/lab/

Has most of the examples in scikit-learn.

TODO: can I run emlearn there?

Takes some 

https://jupyterlite.readthedocs.io/en/latest/howto/pyodide/packages.html

ValueError: Can't find a pure Python 3 wheel for 'emlearn'.

## Stand-alone devices for physical data science

Plug & play.

- Without needing any cloud connectivity.
- Without 

- Keeps the user in control
- 

Aspects

- Measure using sensors
- Store the data
- Connectivity using WiFi
- Discovery using mDNS
- Settings/configuration/control via webui
- Automated continious data processing/analysis. DSP and ML
- Interactive data analysis, served via webui. Lookup, visualization, faceting, clustering
- Raw data storage/sampling, for building/monitoring ML datasets
- Labeling for ML models, via webui. Few-shot learning?
- Optional integration. Pull using HTTP API (same as webui). Push using Webhooks, MQTT

Details

- asyncio concurrency


