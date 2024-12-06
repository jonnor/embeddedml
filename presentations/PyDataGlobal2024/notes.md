
## Outline

- This is a microcontroller, these are its features
- Let us install Python on it!
pip install esptool, download MicroPython, Flash
- OK - how do I program it? Using ViperIDE
- Lets make a sensor! Measure temperature, send to the cloud
- Ooops, I need a library.
Just mip install it / ViperIDE install via "install package via link"

- Lets level up. Doing compute intensive tasks in MicroPython. Sound level meter example.
- Oh no, it is not fast enough in pure Python.
Just mip install the emlearn C module!

- Lets go TinyML. Running a pre-trained ML model. ? HAR
Working outside of ViperIDE. Need to run code on PC also.

- Lets record our own dataset, train a custom model, and deploy
Run recording example on M5StickC
Save data as .npy with npyfile
Tranferring from device with mpremote
Run training on PC
Copy model back

Honorable mentions. Out-of-scope

- Image classification.
- Labeling properly. With LabelStudio
- Event recognition. Like counting exercises repetitions.


## Take aways

- Modern microcontrollers are very powerful and accessible
- MicroPython is a productive and fun way to program them
- Can use the mip package manager to install Python and C modules 
- emlearn-micropython can be used for efficient DSP and ML
- Can build devices that process and analyze sensor data,
such as accelerometer, audio, image

## TODO follow-ups

- Update HAR README to include how to collect data, train model
- Write BLE advertisement example for HAR on M5StickC. Sleeping as much as possible
- Test/fix sound example for T-Camera S3
- Test/fix camera examples on T-Camera S3
- Make a YouTube video for HAR example.


## Microcontroller

Around the power of Intel 368 / 468
1992 cost 1000 USD. Over $2000 in 2024 dollars.

Or an Amiga 4000
https://www.waveshare.com/esp32-s3-zero.htm?sku=25081
6 USD

ESP32-S3FH4R2
2.5 USD


## Device examples
Recommend *ESP32* or *ESP32 S3*.
RISC-V not as well supported yet. ESP32 C2/C3/C5/C6, ESP32 H2, ESP32 P4

- M5StickC PLUS 2
- TTGO T-Camera S3


## Example 1 - temperature sensor


## 

- Make a pretrained execise model for M5StickC PLUS 2 ?
Record a basic dataset.
Strap M5StickC to the arm
Gestures need to be labeled precisely. Also needs post-processing.
And RF is not really the best model for it.
So excercies are better. Counting left as an |excercise| for the reader
- Is gravity removal needed??


# Aside - YouTube video - TinyML zero to hero
From nothing to running a (premade) TinyML example.
With MicroPython, emlearn and ViperIDE - on ESP32.

Script.

- Select a ready-made device. ESP32. LilyGO / M5Stack
- Order it. Online. Wait some days
- Unbox. Plug it in. Shows USB device
- pip install esptool
- Flash with esptool
- Open browser, Chromium based. ViperIDE
- Connect to device - MicroPython terminal. Make LED blink?
- Open example. Ideally a ready-made inference thing
- Test it out
- Switch to data recording
- Train the pipeline

Maybe do one for Human Activity Recognition?


