
# Hardware accelerator for Decision Tree Ensembles

Developing an hardware accelerator for decision tree ensembles ([Random Forest](https://en.wikipedia.org/wiki/Random_forest) etc).
With the eventual goal of taping out as an ASIC via the [Tiny Tapeout](https://tinytapeout.com/) project.
An intermediate goal is to have the accelerator running on an ICE40 FPGA board.

Caveat: This is my first FPGA project since university classes.
Newbie mistakes and bad practices are likely!

## Status
**Concept design only**. Implementation not started.

- First version(s) are intended to be functional demonstrators only. Not optimized for performance or power.
- Some initial research has been done
- System architecture in sketch phase
- No code yet

## Motivation

Running Machine Learning inference directly on (MEMS) sensors is attractive
for TinyML applications to reducing the amount of data that needs to be transported,
which typically has power efficiency benefits.

We would like to research how one could implement modular hardware-acceleration blocks,
and how this may enable better power efficiency than a general-purpose microcontroller CPU.
This includes both feature extraction as well as classification modules.

As the classifiers we are focusing on decision tree ensembles,
as these are quite powerful, computationally efficient,
and may be suited for a compact implementation in hardware.

Usescases we are interested in evaluated include Human Activity Detection using accelerometer,
and potentially Sound Event Detection using microphone. 

## More

See [notes.md](./notes.md) for the work-in-progress
