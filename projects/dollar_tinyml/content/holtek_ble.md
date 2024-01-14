
# BLE beacon 20 cents - the Holtek BC7161

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
