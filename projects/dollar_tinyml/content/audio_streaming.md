
TLDR: Audio data can be streamed to computer over serial to USB,
and using a virtual device in ALSA etc,
we can record from the devices as if it was a proper audio soundcard/microphone.

In a previous post we described the audio input of the prototype board based on Puya PYF003.
LINK
It consists of a 10 cent analog MEMS microphone, a 10 cent operational amplifier, and internal ADC of the PY32.
To check the audio input, we need to be able record some audio data that we can analyze.

The preferred way to record audio from on a microcontroller system would be
to implement audio over USB using the Audio Device Class, and record on a PC (or embedded device like RPi).
https://www.usb.org/document-library/usb-audio-devices-release-40-and-adopters-agreement
This ensures plug & play with all operating systems, without needing any drivers.

Alternatively one could output the audio from microcontroller on a standard audio procotol such as I2S, and then use a standard I2S to USB device to get the data onto the computer.
https://www.minidsp.com/products/usb-audio-interface/usbstreamer

However the Puya PY32 (and most other sub 1 USD microcontrollers), does not support USB nor I2S.
So instead we will stream the audio over serial, and use a serial-to-USB adapter to get it on the PC.
This requires some custom code, as there are no standards for this (to my knowledge at least).

### Streaming audio over serial

Since the serial stream is also our primary logging stream,
it is useful keep it as readable text.
This means that binary data, such as the audio PCM must be encoded.

There are several options here. I just went with the most widely supported, base64.
https://en.wikipedia.org/wiki/Base64
It is a bit wasteful (33% increase), but it is good-enough for our usages.

A default baudrate of 115200 in PY32 examples, on the other hand, will not do.
The bandwidth needed for 8kHz sample rate of 16 bit PCM, base64 encoded is at least 2*8000*(4/3)*8 = 170 kbaud.

Furthermore the standard printf/serial communication is blocking:
So any time spent on sending serial data, is time the CPU cannot do other tasks.
It would probably be possible to setup DMA buffering here, but that would be additional complexity.

I tested the PY32 together with an FTDI serial-to-USB cable working at up to 921600 baud, which is ample.

Example: Serial messages
```
audio-block seq=631 data=AAD///7/AgAAAP3//f/8//3/AwACAAYAAAD//wAAAgAAAAgAAAD//wAA///+/wIA///+//7///8CAAAACAD///3////8/wMA//8AAAIAAgD9/wEACAAAAAEAAAAGAAAAAAACAP//BAD9//3/FwABAP7///8AAAQA/v8CAP7/AAD9/wEA/f8GAAIAAAD6//3/AAAHAAQA+f/e/wEA/v8AAAAA/v/+//3/AAAGAAIAAAD+/wYAAAABAP//AAAAAP7/AAD+//r//v/+/wEA/f/9/wAA/f/+////AAABAAYAAAD9/wAAAQABAAAA/v8GAAAAAQD+/wAAAAAAAAwAAgAAAA== 
```


Receiving is the data done with a Python script, using pyserial.
It identifies which of the serial messages are PCM audio chunks, and then decodes and processes them.
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

```
python User/log.py --device 'hw:3,0'

arecord -D hw:3,1 -f S16_LE -c 1 -r 8000 youtube-speech.wav
```

IMAGE: screenshot of device showing up in Audacity or similar

Note: There is nothing ALSA specific about the Python code,
so this approach should also work with other sound systems that has virtual devices.
Such as PulseAudio/PipeWire on Linux, or on Mac OS or Windows.

### Audio recording using ADC with PY32

Audio recording must be done at high samplerates (8kHz+) and at precise timing (no/minimal jitter).
For that we use the timer pheripheral in the PY32, and wire it up directly to the DMA subsystem.
This way our CPU and program is not involved at all in sampling,
and we get the data as convenient blocks in a size we specify (ex: 64 samples).
This is pushed onto a queue in the DMA interrupt, and can be processed at a leisurely pace in the main loop.

We used this example in the PyF0 template repository as starting point.
https://github.com/IOsetting/py32f0-template/tree/main/Examples/PY32F0xx/LL/ADC/ADC_SingleConversion_TriggerTimer


### Recorded audio

The following audio was recorded by playing back a song on a phone,
with the headphone jack connected to the ADC of a standard PY32F003 development board.

IMAGE: testing setup
EXAMPLE: audio recorded from the device


### Next

And to run some test of the audio input including the on-board amplifier and microphone,
to have some basic measurements of the frequency response, sensitivity, and noise floor,


