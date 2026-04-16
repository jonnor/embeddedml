
# TODO

Project/demos

- On-device time-series database
- Showing EDA in browser. Interactive analysis
- On-device inference with Random Forest
- Export data via API. Analyze data in JupyterLite. Push data back via

TODO

- Finish overall disposition

Maybe slides

- Deployment targets. PC (x86_64), browser (WASM), device (ESP32)
- More info. Add references to Wireless from Krakow 2025

Optional slides

- Generators for data streaming with MicroDot.
To support larger-than-RAM. ! no async def in MicroPython
?? does it actually let our sensor loop run
?? does it work correctly when sending large files with send_file
Maybe do some controlled tests/examples?

Future work - for emlearn-micropython / in browser

- Test training of RandomForest using Jupyter Lite.
- Integrated classifier training with emlearn_extratrees
https://github.com/emlearn/emlearn-micropython/pull/45/changes

Limitations right now

- Power management. Not using power saving.
Can refer to Peter Hinch alt asyncio. ! not tested
- WiFi management. Manual via mpremote. Only joining existing network
MicroPython also supports device creating network.
? link to exiting WiFi management libraries
- Time-series compression. First version got no savings on real data.
Needs further investigation. Probably quantization of features.

Documentation

- emlearn-micropython. Add getting started for web/browser.
Simple example for inference.
Add to the README.
- emlearn-micropython. Check that 2025 presentations are linked in docs


# Planning

## Takeaways

- MicroPython enables physical computing for those that know Python
- Applicable to many data-oriented applications. Especially those incorporating sensors
- MicroPython enables scaling down to hardware that costs 10 USD
- emlearn-micropython enables running machine learning models. Both inference and learning
- Can also run in the browser. Interactive, data visualization, etc
- MicroPython in browser enables serving from device. Faster loading compared to big Python
- asyncio enables concurrency

## What was promised

- Measuring the surroundings using sensors
- Connectivity using WiFi
WiFi credential management
- Data storage using on-board filesystem
Time-series storage
- Serving a webui for configuration/control, using Microdot
API to download data
- Automated data processing/analysis using DSP and ML, with emlearn-micropython
Known feature extraction
Motion classifier using Random Forest
Pretrained models?
- Enabling interactive data analysis via webui
Browsing timeseries. Selecting sections, comparing. Using Plotly?
- Managing concurrency on microcontroller, using asyncio
Cooperative scheduling. Deadlines. FIFO
- Optional integration. Pull using HTTP, and/or push using Webhooks/MQTT


## Disposition

Format. 20-25 minutes + QA.
20-25 slides.

Goal

- You as a Python developer will learn
how to build stand-alone IoT devices for measuring and analyzing physical sensor data
using MicroPython and emlearn

Introduction. 2 min

- About Soundsensing
- Goal/structure of this talk
- What is MicroPython
- Data science with MicroPython
- About emlearn-micropython
Goal of project. Make it super easy to. Data science for physical data.
Including machine learning on-device etc.
Like a scikit-learn for microcontrollers. And then building supporting pieces needed

Case introduction. 3 min

- What we will build.
Activity tracker "smartwatch" for Pythonistas that are crazy about data
Local-first. Data ownership. Full control/access. Easy setup.
- The hardware. What is a microcontroller.
- MAYBE:  IoT architectures alternatives. From physical to device to user in UI.
- The software stack (overview). System block diagram.
Device - data processing + web server. Frontend (browser).

On-device time-series database. 5 min

- Web server. With microdot
- Concurrency model. asyncio.

On-device inference with emlearn-micropython. 5 min

- HAR features?

Browsed based ML with emlearn-micropython. 5 min

- emlearn-micropython now runs in browser
.wasm and .mjs files
External C modules
TODO: add documentation

- PCA

Use data in other environments. 3 min
 
- Pull from HTTP API, with a URL. CURL command or Python
- Push to phone via BLE
- Push to HTTP or MQTT.
!? make sure to enable timeout on the socket
Keep the data to send in a queue. Only remove from queue after successful send
https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py
https://docs.micropython.org/en/latest/library/socket.html

Outro. 2 min

- Call-to-Actions
If you are interesting in running ML/DSP on microcontroller or in browser,
check out emlearn-micropython. There are many other talks linked in documentation


# Feasibility

The big questions

Can we...
- Run ML models directly on device?
Yes. Established from earlier. With emlearn-micropython.
Previous talks about it at EuroSciPy etc

- Store a sufficient amount of data on device?
Want 24 hours of raw data.
And several weeks of activity detections.

Able to store up to 24 hours of raw 3-axis int16 at 25 Hz.
3*2*3600*24*25/1e6 = 12.96 MB

Implemented time-series compression with Simple9b and delta-encoding. 128bytes
! did not help. Compression savings around as overhead. No net gain. 

- Provide an interactive web ui for seeing time-series data.
Yes. With microdot project.
But will there be enough space?
Plotly "minimal" only takes around 300 kB. Check

- Load the data fast enough in WebUI.
Loading time should be a few seconds
Able to load around 0.1 MB per second. 4kB sizes
! had hoped for 1.0 MB per second.
Might be bottlenecked by FLASH hardware, not MicroPython

- Access the data from other devices?
Yes. Via HTTP API.
! CORS is critical. MicroDot has built-in support for this
LLM did not know about this. Spent a lot of time re-implementing it in buggy ways
Sometimes just reading the documentation is the best...

- Can we run ML algorithms in browser using MicroPython?
Yes. PCA is working.
! No dynamic native modules (.mpy) in Webassembly port of MicroPython.
https://github.com/emlearn/emlearn-micropython/issues/41

All C modules must be included in the build.
Slightly different interface. Possible to do both with some ifdefs
WIP: RandomForest training module for emlearn, to do training in browser. MR
https://github.com/emlearn/emlearn-micropython/pull/45





# Status

- All the feasibility checks passed.
- Got emlearn-micropython working in browser
- Data pipeline on device has been setup

TODO
- Implement device UI


# Notes

## MicroPython and emlearn in browser

- Make a browser demo for inference. Basically same kind of model as on device.
- Browser demo, heavier model, running on instances on-device model flagged of interest
- Make a browser demo for labeling
- Make a browser demo of training
- Make a browser demo for train-in-browser + deploy-on-device

## Stand-alone devices for physical data science

Plug & play.

- Without needing any cloud connectivity.
- Without needing any server setup on local network
- Keeps the user in control
- Easy onboarding

Aspects

- Measure using sensors
- Store the data
- Connectivity using WiFi
- Discovery using mDNS
- Settings/configuration/control via webui
- Automated continious data processing/analysis. DSP and ML
- Interactive data analysis, served via webui.
Lookup, visualization, faceting, clustering
- Raw data storage/sampling, for building/monitoring ML datasets
- Labeling for ML models, via webui. Few-shot learning?
- Optional integration. Pull using HTTP API (same as webui). Push using Webhooks, MQTT

Details

- asyncio concurrency


## Ideas

Concepts

- Serve MicroPython WASM from device. For analysis/training in browser. YES
- Doing Exploratory Data Analysis in browser. YES
- Doing data labeling in browser. LATER
- Doing data curation/cleaning in browser. LATER
- Doing training in browser. LATER

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

Data analysis techniques

- Search for motifs? Repeating occurrences
- Search for anomalies?
A MatrixProfile implementation for MicroPython would be fun!?
- FFT analysis. Spectrograms. Compare spectrums between different sections of time
- Histogram analysis. Compare distributions between different sections of time?


# Tests and learning

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

## HTTP testing from RAM

Using ESP32 pico in M5StickC PLUS 2 over WiFi

$ for chunk in 1024 2048 4096 8192 16384 32768 65536; do curl -s "http://192.168.87.152:5000/stream?chunk=$chunk" -o /dev/null -w "chunk=$chunk: HTTP %{http_code}, Size: %{size_download} bytes, Time: %{time_total}s, Speed: %{speed_download} bytes/s\n" --max-time 60; done
chunk=1024: HTTP 200, Size: 524288 bytes, Time: 3.901785s, Speed: 134371 bytes/s
chunk=2048: HTTP 200, Size: 524288 bytes, Time: 2.629534s, Speed: 199384 bytes/s
chunk=4096: HTTP 200, Size: 524288 bytes, Time: 1.776227s, Speed: 295169 bytes/s
chunk=8192: HTTP 200, Size: 524288 bytes, Time: 2.624618s, Speed: 199757 bytes/s
chunk=16384: HTTP 200, Size: 524288 bytes, Time: 3.488393s, Speed: 150294 bytes/s
chunk=32768: HTTP 200, Size: 524288 bytes, Time: 5.452071s, Speed: 96163 bytes/s
chunk=65536: HTTP 200, Size: 524288 bytes, Time: 4.939647s, Speed: 106138 bytes/s
Now streaming 512KB. 4KB chunk wins at 295 KB/s, then 2KB at 199 KB/s. Performance degrades significantly with larger chunk sizes.

Would take 16 seconds for 4 MB of data.
Not fast enough to be done in once go.
Needs to be background and iterative.

## HTTP testing from disk/FLASH

First version

Results:
| Chunk | Time | Speed |
|-------|------|-------|
| 1024 | 8.18s | 64 KB/s |
| 2048 | 5.31s | 99 KB/s |
| 4096 | 3.64s | 144 KB/s |
| 8192 | 4.35s | 121 KB/s |
| 16384 | 9.07s | 58 KB/s |
| 32768 | 7.54s | 70 KB/s |
| 65536 | 8.30s | 63 KB/s |

accidentially read continiously for as long as request open

chunk=1024: Size: 3309568 bytes, Time: 30.000507s, Speed: 110317 bytes/s
chunk=4096: Size: 9334784 bytes, Time: 30.000009s, Speed: 311159 bytes/s
chunk=8192: Size: 4114176 bytes, Time: 30.001165s, Speed: 137133 bytes/s
chunk=16384: Size: 2172032 bytes, Time: 30.000515s, Speed: 72399 bytes/s

With fixed termination.

File-Stream Benchmark Results:
| Chunk | Size | Time | Speed |
|-------|------|------|-------|
| 1024 | 512KB | 6.06s | 87 KB/s |
| 2048 | 512KB | 4.11s | 127 KB/s |
| 4096 | 512KB | 3.23s | 162 KB/s |
| 8192 | 512KB | 3.49s | 150 KB/s |
| 16384 | 512KB | 6.41s | 82 KB/s |
| 32768 | 512KB | 9.36s | 56 KB/s |

Seems like 150 kB/s is best we can do for now.


There are some benchmarks for LittleFS on ESP32 at
https://components.espressif.com/components/joltwallet/littlefs/versions/1.20.4/readme

```
Reading 5 88KB files
LittleFS (cache=512 default):   5,874,931 us
LittleFS (cache=4096):          5,731,385 us
```
That is around 88kB per second.

### What is a good chunk size?


### What is a good layout

resource-then-time is flexible for different partitioning layouts
But with multiple resources will have to duplicate
Also - supporting different partitioning schemes will need more/general code, room for bugs

## Codename
microhive

## Partition layput

Hive-style partitioning.

```
date=2026-01-01/
    a_daily.npy
    hour=08/
        a_metrics.npy
        min=34/
            a_raw.npy
```

## Resource metadata

Each resource has:

- An identifier/name. Short, since needs to be in files
- A hop. In microseconds. Used to compute time offsets from time values
- An ordered list of column names.
- A dtype. Must initially be int16

## Time representation
Time column in files are optional.
If not present, assumed to be dense: starting from 0 and increasing by 1 for each row.
Time values are multiplied by a resource-wise hop value, in microseconds.
Then this is added to the datetime for the partition to get the absolute timestamp value.
NOTE: time values can be sparse, but must be ordered monotonically increasing.
When possible they should be

## Mixed columnar and row-based
Row-based is best for appending. Just put the latest observation(s) there.
But columnar is best for time-series compression, critical to storage efficiency.
And for selecting particular columns, if needed.

Only allowed to insert row-based at the end.
A compaction process converts from row-based uncompressed to columnar/compressed.
Triggered on append.
Internal details. External users of the timeseries database or API does not need.

Row-based chunks have different file ending than columnar.

## Chunk representation
Numpy .npy is OK for a prototype. row-based.

With .npy files, use 1,2,3 etc as column values. Avoid duplicating them in each file.
Then the real columns are added in the API accessors.

## Filesystem
Typically using LittleFSv2 on device.
Note that in MicroPython, the block size is 4kB.
This means that files have this as a minimum size.

## API

class MicroHive:
def __init__(self, base_dir, resources : dict):

def get_timerange(self, resource : str, start : int, end : int, chunk_rows=DEFAULT_CHUNK_):

    Query seconds Unix Epoch
    Gives a generator. Giving out chunks of array.array, column-major
    chunk_rows  number of rows yielded per generator iteration


def append_data(resource : str, data : array.array)

    Data must have a length which fits with resource
    array is column-major
    Will be inserted at the end

resources = {
    "raw": {
        "hop": 50000,          # microseconds (20Hz = 50ms)
        "columns": ["a", "b"],
        "dtype": "int16",
        "granularity": "minute" # date | hour | minute
    }
}

## Seeking in files

Or use a binary format from scratch?
n_columns

?? is it neccesary to support seeking inside a file
Assuming files are under 100kB each (1 second load), then OK to skip initially.
But would like to support this later - it makes chunk size less critical.


8760 hourly folders for 1 year
10 metrics at 1 second res, 59kB

1440 minute-wise folders for 1 day
At 20hz with 3 cols int16, each file is 7.2kB. 15kB if 6axis

? how fast can MicroPython load 1000x files?

### Other

Yes. Make sure only Python standard library is used, no external dependencies.

And for .npy file reading and writing, use this code

Streaming read
Streaming/chunked reading can be used to keep memory usage low.

### Tests

- Load 1 year of daily-paritioned data, with 1 minute resolution
- Load 1 day of hour-partitioned data, with 1 second resolution
- Load 1 hour of 20hz raw data
- Appending 20hz raw data, in small chunks. With auto-compaction

Key requirement: at no time should any process be blocking for more than 100 ms. 

## HTTP multiple requests

What happens if one browser makes multiple requests? 

## Hardware platform

- M5Stick C PLUS 2. ! PDM mic, not I2S. 8 M FLASH / 2 MB PSRAM
- Lilygo T-Watch ESP32 S3 watch. 16MB FLASH / 8 MB PSRAM
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


## jupyter-lite for scikit-learn

https://scikit-learn.org/stable/lite/lab/

Has most of the examples in scikit-learn.

TODO: can I run emlearn there?

Takes some 

https://jupyterlite.readthedocs.io/en/latest/howto/pyodide/packages.html

ValueError: Can't find a pure Python 3 wheel for 'emlearn'.



