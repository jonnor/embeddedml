
# 1 dollar TinyML

A computer with a modern GPU for machine learning is approx 1000 USD.
The state-of-the-art ML models that in the mainstream attention are getting ever larger.
Currently being led by Large Language Models and Generative Image models.
Requiring more compute and RAM every year.

TinyML is .
Low cost enables massive scale.

What can one get for 1 USD?

Bill-of-Materials (BOM) for a working system.
Assuming 1k volumes.
PCB Assembly (PCBA) costs are not included,
and neighter as mechanical elements.

# TODO

- Move files to embeddedml/projects/dollar_tinyml
- Create project on HackADay, with introduction post
- Create post on sub-dollar microcontrollers
- Create initial schematic
- Create post on tree-based models
- Create post on RNN models
- Get Holtek BLE PoC working
- Create post on holbeacon

# DONE

- Theoretical check that RNN can fit into 2 kB RAM / 32 kB RAM.
Confirmed. FastGRNN etc.

#### Microcontroller

Can get a pretty modern microcontroller for 1 USD.
Even down 0.10 USD. Some options also below this.

- 1x RP2040 chip. Cortex M0+
`1 USD @ 1k`
- WCH CH582F
`0.68 USD @ 1k`.
**BLE** microcontroller
- ATTiny with 4KB FLASH / 512 bytes RAM
`0.4 USD @ 1k`
- STM32G030F6P6 0.30 USD 32 kB FLASH / 8 kB RAM.
With USB!
0.2 mA in LPRUN 2Mhz
5 uA in STOP 1 no SRAM retention with RTC.
`0.30 USD @ 1k`
- WCH CH32V003. RISC-V
16KB FLASH / 2KB RAM.  48MHz QFN-20
`0.15 USD @ 1k`
- PY32F002. Cortex M0+
`0.10 USD @ 1k`
20 Kb FLASH / 3 kB RAM. 24 Mhz
- Padauk PFS154
`0.06 USD @ 1k`
2 kB FLASH / 128 bytes of RAM
- Fremont Micro Devices FMD FT60F011A-RB
`0.06 USD @ 1k`.
- Padauk PMS150C
`0.03 USD @ 1k`
1 kB OTP / 64 bytes of RAM. **One-time-Programmable**

Review of 3 cent MCUs
https://cpldcpu.wordpress.com/2019/08/12/the-terrible-3-cent-mcu/

Flashing tools for low-cost microcontrollers. Implemented in pure Python
https://github.com/wagiminator/MCU-Flash-Tools

Padauk
https://github.com/free-pdk

SDCC C compiler. For tiny/old/odd 8 bit targets
https://sdcc.sourceforge.net/




### Sensors
Prices from JLCPCB

- MEMS microphones `<0.2 USD`
- Photointerruptor 0.1 USD
- LIS2DH12TR accelerometer. 0.3 USD

### Power

Consumable battery

- CR1216 battery at 0.2 USD
- CR2477 `0.8 USD @ 1k`

Rechargable battery

- LIR1220 `0.2 USD @ 1k`. 7 mAh
- Battery charger `0.06 USD @ 1k`
 

### Connectivity

- 315Mhz/433 Mhz. Below `0.1 USD @ 1k`
- BLE. From `0.2 USD @ 1k`

#### Holtek BC7161
BLE beacon IC
`0.2 USD @ 1k`. 
SO8 package
https://www.holtek.com/productdetail/-/vg/BC7161
Communication over I2C

Holtek BC7262
SO10 package
Communication over I2C




### System-view

Could one build an entire application?
Challenge: Power, communication


#### A health wristband
With Human Activity Recognition and pulse monitoring.
Logging to internal FLASH, USB connectivity.

- XySemi XC5011 charger
- Everlight Elec ITR8307/S17/TR8(B)
- STMicroelectronics STM32G030F6P6
- STMicroelectronics LIS2DH12TR
- LIR1220 battery

Total BOM: `< 1.0 USD @ 1k`

7 mAh / 24 hour = 0.29 mA average consumption.
7 mAh / 30 days = 9 uA average consumption.

32 kB FLASH / 8 kB RAM.

16 kB / 4 kB for model.
1 second @ 50 Hz triax = 0.3 kB

32-slot data FIFO. Only need wakeup couple of times per second

#### Smart audio

- MCU. CH32V003. `0.13 USD @ 1k`
- Microphone. LinkMems `0.10 @ 1k`
- BLE. Holtek BC7161 `0.20 @ 1k`
- Analog opamp. `0.10 @ 1k`. Maybe not needed?? With CH32V003
- Power. LIR1220?. Edge USB connector?

Also very constrained for audio with 2 kB RAM.
Probably will use 1-10 mA, for continious listening.
Just 1 hour or so on battery?

But if one can put it in a USB socket somewhere, can do continious monitoring.


### CH32V003

Ch32v003 with Microphone Module and Telemetry Viewer
https://www.youtube.com/watch?v=AnvOQRSDUao

CH32V003 USB support
https://github.com/cnlohr/rv003usb
https://www.youtube.com/watch?v=j-QazXghkLY

2kB RAM. 48 MHz frequency.
Enough for soundlevel computations.
Is it enough for FFT?

CH32V003A4M6 is SOP14

RUN VDD=3.3V internal RC
FHCLK = 48MHz   6.57  4.16 mA
FHCLK = 750KHz  1.11  

SLEEP VDD=5.0V internal RC
FHCLK = 750KHz 0.47 0.43 mA

Sleep wakeup    30 us
Standby wakeup  200 us

ADC sample rate up to 430 kHz

2 opamp inputs, 1 output. 1 single/differential opamp.

https://github.com/sad-electronics/wch-kicad-lbr

## Accelerometers

Silan SC7A20
`0.18 USD @ 1k` LCSC
Supported in Linux Industrial IO driver
Datasheet only in Chinese??
Patch says they are clones of LIS2DH
https://patchwork.kernel.org/project/linux-iio/patch/20200811134846.3981475-3-daniel@0x0f.com/

https://wiki.analog.com/software/linux/docs/iio/iio
https://github.com/analogdevicesinc/pyadi-iio
https://wiki.analog.com/university/labs/software/iio_intro_toolbox#pyadi-iio
Shows AXL345 accelerometer on Raspberry PI as example

## Microphone

### Analog microphone

https://www.lcsc.com/products/Audio-Components-Vibration-Motors_385.html
Both MEMS and elecret microphone below 0.1 USD

MEMS microphones down to 0.03 USD @ 1k

LMA2718B381 / LMA2718T421
200μA, -42 dB sensitivity

Elecret examples

INGHAi GMI6050
INGHAi GMI9767

Might want to have analog opamp, to not rely on WCH uC opamp.

SOT23-5 options under 0.1 USD
https://www.lcsc.com/products/Operational-Amplifier-Comparator_515.html

COS6001, LMV321IL
50 uA current consumption


# Power

## Lipo battery chargers

Many options below 0.1 USD
https://www.lcsc.com/products/Battery-Management-ICs_612.html?keyword=battery%20charger
Typically in SOT23-5 package
GX4054, LTH7R, LR4054A-T
3000 pcs reel down to 33 USD.


## Weight measurement

Strain gauge BF350-3AA, 0.30 USD @ 100 pcs
Need a Weatstone bridge and opamp for signal conditioning.
Plus needs to be attached to an elastic bar that experiences strain.
Can probably be FR4 PCB structure.


#### IoT sensor
BLE beacon

#### NRF52 with accelerometer
HolyIoT or similar.
7 USD @ 1
5 USD @ 1k

Not yet 1 USD. But `<< 10 USD`.

Sensors 100x 7 = 700
IoT gateway. 100 USD.

Conclusion:
One can get system with 100 ML-enabled sensors for price of 1 RTX3090

But 16 kB RAM and 192 kB FLASH.
How to run ML on this?
And what is feasible vs infeasible?


## BLE beacon 20 cents - the Holtek BC7161

Blogpost candidate.
Would be best to include a demo. But could do a Part I and a Part II
Submit it to HackADay. Maybe put 1 dollar TinyML sensor as project there also.
Submit to the .... forums where people post about

Outline

- Ultra cheap IoT
- Sending sensor data using BLE
- Holtek chip - what is it, how it works
- 

### TLDR
Ultracheap 20 cent chip for creating BLE beacons with any microcontroller - the Holtek BC7161

### Ingress

The prices of electronics hardware and Internet-of-Things (IoT) technology is continuing to drop.
For example, one can get microcontrollers for under 20 cents USD that have 2KB+ RAM and 16 kB+ FLASH.
This matches or is better than than the classic ATMega32 known from Arduino Uno.
Popular candidtes include WCH CH32V003, PY32F002, and Padauk PFS154.
LINKS

And it turns out, there are now 

While scanning LCSC I came across the 20 cent USD

I came across this when researching how cheap it is possible to transmit sensor data,
as part of a quest to create a Machine Learning system for under 1 USD total.
LINK 
I have not seeen much written about it so far, so I thought I would document the finding here a bit.

 https://www.lcsc.com/

This has not been written much about yet, so I thought it.
Recently I found a Bluetooth Low Energy (Bluetooth LE / BLE)


### Sending sensor data as BLE advertisements

? maybe split into two sections - first main motivations.
Then underlying tech and best practices. Could also refer to another off-site post.

BLE advertisements are used in BLE beacons.
Traditionally used for static data. And basis for discovery.
Indoor positioning. Asset tracking. Find my X.
Couple of different standard formats for beacons
But can be used for dynamic data.

IMAGE. BLE advertisement data structure. 

One-way-communication without guaranteed delivery
Lots of off-the-shelf examples of this
Note: data is transmitted plain, no built-in encryption mechanism
Would have to be done in the application layer
In practice can send XX bytes
Probably want to have a sequence number

Since no guaranteed delivery, want to resend each packet a few times
Retransmission guidelines


### Quick introduction to Holtek BC7161

BC7162 / BC716x ? 

Not just a really amazing price.
Also has features that makes it super simple to use.

IMAGE module options
LINK datasheet
LINK website
LINK where I bought it

I2C. Can be used with ANY microcontroller.

Super because it allow to pick the best microcontroller.
Or just the one one is most famililiar with.
Or already used on in a project, adding BLE seamlessly.

For example, at Soundsensing we work a lot with sound.
And the STM32L4 is one of the absolute best at low-power digital sound from PDM microphones
Could even use an FPGA - which typically does not.

Simple protocol. Just set a few registers with configuration, and then transmit the.
Automatic handling of power states.



### Sending some data from a Arduino

I have a bunch of old Arduino/ATMegas around (like many others, I am sure).
So lets use that for testing.

CODE. Arduino class for Holtek

? keep this with some existing hardware/MCU
A non-BLE enabled one is most relevant.
Atmega32 ? 
To be replaced by

Use IMU like MPU

Orientation
Temperature

BONUS: use the data for something. Keep it simple / funny
Like a 6 sided die that one can roll. 3d-printed
Arduino Pro Micro. 33 mm long
Updates advertisement data on change.
Send on change, or every 30 seconds?
Maybe blink the LEDs on transmission

### Next

Next steps in the 1 dollar TinyML project

Could this be it?

Human Activity Detection is a candidate

