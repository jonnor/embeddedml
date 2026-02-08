
## Format

45 minutes presentation.
Plus a 15-minute moderated Q&A.

## Target audience

- Developers working with microcontrollers, sensors and embedded Linux
with an interest in real-time capability, portability, driver development and toolchains
- IoT architects & system integrators with a focus on connected devices, edge computing and cloud integration
as well as an interest in network protocols, energy efficiency and over-the-air updates
- Security experts and specialists in secure firmware, trusted execution environments and cryptography.
with an interest in secure boot, TLS, hardware acceleration and post-quantum cryptography
- Tool and hardware vendors of boards, debuggers, IDEs and toolchains
with an interest in integration topics and driver support

## TODO

- Data collection
Add bit about storing to CSV

- Validation
Explain running entire pipeline on PC
Explain running entire pipeline on device

- Toothbrush project.
Mention steps.
MicroPython + ESP32. January 2025.
MicroPython + Zephyr + NRF52
C + Zephyr + NRF52
C + Zephyr + WCH CH32V006
Add pictures of improved hardware

- Oil spectrometer
Add example slide
https://github.com/jonnor/spectrometer/

Maybe

- Add build system integration. CMakeLists.txt
- Improve spectrometer project README

Later

- Fixup missing parts in motion_recognition example
- Re-test toothbrush on Zephyr+MicroPython.
- Check the QA from OSSummit, consider integrating some of that in slides


## Review OSSummit slides

Concept

- Reading sensors
- Creating dataset
- Training model
- Deploying model
- Validating

Weak

- Validation. Completely missing!
Example of reading from CSV, full pipelines, output + checking.
Maybe process.c can be starting point
- Train. Have C preprocessor
- Train. Use C preprocessor in har_train.py
- Reading sensors. Missing storage. Could use CSV. On USB disk?
- Reading sensors. Missing C code example for RTTI
- Reading sensors. Missing C code example with I2C FIFO direct. Maybe put into toothbrush?

Possible

- Add a bit on optimization of models?
- Add a simpler example? 1 in - 1 out. Spectrometer?

Examples

- HAR feature extractor in C. Enough for toothbrush at least.
- Gravity subtraction in C using eml_iir. Incorporate into process.c
- Run HAR pipeline on C preprocessed data from CSV files.
See sensor_reader/tools/process.c


## Dream design Zephyr emlearn

- Data recording example/entrypoint
- Model validation example
- Live running example
- Training examples. Mostly exist in har_train.py

