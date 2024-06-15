
In a previous post we described the audio input.
LINK
It consists of a 10 cent analog MEMS microphone, a 10 cent operational amplifier, and internal ADC of the Puya PY32.
Now we need to verify that this audio input works, and has sufficient quality.

Our goal is to be able to capture speech, music and general sounds well
enough to do practical ML tasks.
That the audio sounds good to the human ear is not important.

For Machine Learning it is critical to have (at least some) data from the device we deploy on.
This is because the particular characteristics of the device,
such as the frequency response and noise of the microphone/audio subsystem,
influence the data in a considerable way.
We as humans are great at ignoring inconsequential differences, but this property does not come automatically in ML systems.
Failing to account for this can lead to an ML model that works well in training and evaluation,
but performs much worse in practice when deployed.

The preferred way to record audio from on a microcontroller system would be
to implement audio over USB using the Audio Device Class, and record on a PC (or embedded device like RPi).
https://www.usb.org/document-library/usb-audio-devices-release-40-and-adopters-agreement
This ensures plug & play with all operating systems, without needing any drivers.

Alternatively one could output the audio from microcontroller on a standard audio procotol such as I2S, and then use a standard I2S to USB device to get the data onto the computer.
https://www.minidsp.com/products/usb-audio-interface/usbstreamer

However the Puya PY32 (and other sub 1 USD microcontrollers), does not support USB nor I2S.
So instead we will stream the audio over serial, and use a serial-to-USB adapter to get it on the PC. This requires some custom code, as there are no standards for this (to my knowledge at least).

### Streaming audio over serial

Since the serial stream is also our primary logging stream.
Therefor it is useful keep it as readable text,
and this means that binary data, such as the audio PCM must be encoded.

There are several options here. I just went with the most widely supported, base64.
https://en.wikipedia.org/wiki/Base64
It is a bit wasteful (33%) increase, but it is good-enough for our usages.

A default baudrate of 115200 in PY32 examples will on the other hand not do.
!!! Bandwidth needed is at least
I tested the PY32 together with an FTDI serial-to-USB cable working at 921600, which is ample.

IMAGE: serial message

Receiving is done with a Python script.
It identifies which of the serial messages are PCM audio chunks.
These are decoded and processed.
Other messages from the microcontroller are logged out as-is.

### Virtual soundcard using loopback

Getting the audio into our script on the PC side is useful.
But preferably we would like to use standard audio tools, and not have to invent everything ourselves.

So we take the received audio data, and write it to a sound device, using the sounddevice library.
https://python-sounddevice.readthedocs.io/

This allows playing it back on our speaker, which allows for simple spot checking.
But even more useful is to use a loopback device, to get a virtual sound card for our device.

I tested this using ALSA loopback
Ref https://sysplay.in/blog/linux/2019/06/playing-with-alsa-loopback-devices/

Can then record using any standard program that supports ALSA (which is practically everything on Linux).

EXAMPLE: recording in Audacity, sinewave waveform

Note: There is nothing ALSA specific about the Python code,
so this approach should also work with other sound systems.
Such as PulseAudio/PipeWire on Linux, or on Mac OS or Windows.

### Audio recording using ADC


A timer for sampling at.
And DMA for buffering the data.
This allows to easily do processing of audio while handling the data from the input stream.

Used this example in the PyF0 template repository as starting point.
https://github.com/IOsetting/py32f0-template/tree/main/Examples/PY32F0xx/LL/ADC/ADC_SingleConversion_TriggerTimer



### Demo


EXAMPLE: speech recorded on the device


### Next

Now we got audio coming in, and we know that it is of reasonable quality.
We will need to implement some audio feature extraction, and then an ML classifier.


