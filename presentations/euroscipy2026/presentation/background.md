
## Hardware platform

- M5Stick C PLUS 2. ! PDM mic, not I2S. 8 M FLASH / 2 MB PSRAM
- Lilygo T-Watch ESP32 S3 watch. 16MB FLASH / 8 MB PSRAM
- T-Camera V3 2020. ! obsolete
- T-Camera S3. Missing PMU code. 16MB FLASH / 8 MB PSRAM
- XIAO ESP32S3 Sense. Includes SDcard. ! PDM mic, not I2S
- Raspberry Pi Pico W. 2 MB of on-board QSPI (RP2040 max 16 MB). 264kB RAM
- Pico 2 W. 4 MB of QSPI flash (RP2350 max 16 MB). 512 kB RAM
- ESP32 Pico 8 MB typical

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



