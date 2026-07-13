
# About

https://pretalx.com/euroscipy-2026/talk/ZT3BMR/

# Format
20 minute slot. 15 minutes + 5 minutes QA.
! SHORT. Need to be very efficient in disposition.

# Goals

- Show off emlearn-micropython browser support
- Show off emlearn-micropython training support
- Become a teaching platform for data-centric ML training.
Enabling people to make things that handle custom applications easily.
Can do a lot just from a web interface

# Overall status

- All the feasibility checks passed.
- Got emlearn-micropython working in browser
- Data pipeline on device has been setup

TODO

- Implement the different demos
- Make sure slides present the project well

# TODO

Project/demos

- Move timeseries database code to dedicated repository. mip installable
https://github.com/jonnor/micropython-tsdb
- emlearn-micropython. Add getting started for web/browser.
Simple example for inference.
Add to the README.
- emlearn-micropython. Check that 2025 presentations are linked in docs

Slides

- Redo overall disposition. DEMO led. CUT to fit 15 minutes
Refer to existing projects and presentations where possible

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
- Data storage using on-board filesystem
Time-series storage.
- Serving a webui for configuration/control, using Microdot
API to download data
- Automated data processing/analysis using DSP and ML, with emlearn-micropython
Known feature extraction
Motion classifier using Random Forest
Pretrained models? NO/Later
- Enabling interactive data analysis via webui
Browsing timeseries. Using Plotly.
Plot overall. Selecting sections, comparing
- Managing concurrency on microcontroller, using asyncio
Cooperative scheduling. Deadlines. FIFO
- Optional integration. Pull using HTTP, and/or push using Webhooks/MQTT
- Connectivity using WiFi
Basics are in place
SKIP. WiFi credential management
SKIP. WiFi dynamic enable/disable

## Disposition

Format. 15 minutes + QA. 15 slides.
DEMO led.

Project/demos

- On-device time-series database
- Showing EDA in browser. Interactive analysis
- On-device inference with Random Forest
- Export data via API. Analyze data in JupyterLite. Push data back via

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

Case introduction. 2 min

- What we will build.
Activity tracker "smartwatch" for Pythonistas that are crazy about data
Local-first. Data ownership. Full control/access. Easy setup.
- The hardware. What is a microcontroller.
- MAYBE:  IoT architectures alternatives. From physical to device to user in UI.
- The software stack (overview). System block diagram.
Device - data processing + web server. Frontend (browser).

On-device time-series database. 2 min

- Benchmark results?
- Web server. With microdot
- Concurrency model. asyncio.

Browsed based ML with emlearn-micropython. 5 min

- emlearn-micropython now running in browser
.wasm and .mjs files
External C modules
TODO: make examples/demos
TODO: link documentation
- PCA. Part of motion-machine.
MAYBE: Move into emlearn-micropython ?
NOTE: Not accelerated with C at the moment

On-device inference with emlearn-micropython. 2 min

- HAR features?
Refer to existing materials. Examples in emlearn-micropython & presentations

Use data in other environments. 3 min
 
- Pull from HTTP API, with a URL. CURL command or Python
- Pull into Jupyter Lite for full Python experience
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




# Notes

## MicroPython and emlearn in browser

- Make a browser demo for inference. Basically same kind of model as on device.
- Browser demo, heavier model, running on instances on-device model flagged of interest
- Make a browser demo of training
- Make a browser demo for labeling. Simple 2d thingy?
- Make a browser demo for train-in-browser + deploy-on-device

## Ideas

Concepts

- Serve MicroPython WASM from device. For analysis/training in browser. YES
- Doing Exploratory Data Analysis in browser. YES
- Doing data labeling in browser. LATER
- Doing data curation/cleaning in browser. LATER
- Doing training in browser. LATER

Usecases

- Wearable device. FOCUS
- Lab gear. For scientific/engineering uses
- Wireless Sensor Networks. Ref EuroScipy Krakow 2025
- Educational lab exercises.
- Robotics.
- DIY/Maker/kits. For niche cases. Or open-ended.

Demos

- FOCUS. Motion classification

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

