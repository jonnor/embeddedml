
# microvad

A microscopic Voice Activity Detection for microcontrollers.

## Voice Activity Detection

Voice Activity Detection (VAD) is the task of detecting the presence of human voice.
It is also known as Speech Activity Detection,
and a closely related task is Speech Segmentation.

A Voice Activity Detection is often a component of a larger speech processing systems
that do for example Automatic Speech Recognition (ASR) / Speech to Text (STT),
Speaker Recognition, Speaker Diarization et.c.

## Status
**Not useful yet**

In early development. See [TODO](./TODO.md)

## About

`microvad` is designed for low-power and compute constrained microcontrollers.

- Low-latency detection (50ms)
- Primarily for medium to low degrees of noise (SNR of +5 dB or better)
- Works with as little as 1kB RAM and 10 kB of program memory / FLASH
- Consume as little as 5% CPU on standard microcontroller
- Better quality detections than existing tiny open-source models Example: WebRTC VAD
- Is geared primarily towards speech (not singing voice)
- Tunable operating point. Select False Trigger / False Accept balance
- Runs on all modern 32-bit devices. ARM Cortex M, ESP32, RISC-V, et.c.
- **Might work** on 8-bit / 16-bit devices
- Runs in any environment with a C99 compiler
- No dynamic allocations (malloc/free)

microvad is implemented using the [emlearn](http://emlearn.org) Machine Learning library.


### What to use it for

When you need to do Voice Activity Detection on a small microcontroller or embedded device.

Some example applications could be

- Low-power frontend for a Speech Recognition systems.
- Battery-powered wearable devices that react on speech presence
- Avoiding picking up human voice in Wireless Sensor Networks

### When NOT to use it

If any of the following are true, you probably should consider using something else.

- Have more than 1MB of RAM
- Running on regular computer
- Do not need low-power
- Do not need low-latency
- Need good performance in high noise / low SNR cases
- Want to track singing voice / vocals in music

For these cases there are other alternatives, which might serve you better.
Notable open-source altenatives models include
[SpeechBrain VAD](https://huggingface.co/speechbrain/vad-crdnn-libriparty)
and [Silero VAD](https://github.com/snakers4/silero-vad).

If latency or compute power is not a major contraint,
it is also an option to use a *Automatic Speech Recognition* (*Speech to Text*) software to do
Voice Activity Detection / *Speech Detection* / *Speech Segmentation*.
There are many open-source alternatives for this.
One example would be to [use VOSK](https://github.com/jonnor/machinehearing/tree/master/handson/speech-segmentation-words).

## License
microvad is licensed under the MIT license

## Documentation
Once the project is useful!


