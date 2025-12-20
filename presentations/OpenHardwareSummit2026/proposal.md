
# Proposal

## Format

IN PERSON TALKS: 20 minutes in-person talks

## Title

Digital audio on open silicon with Tiny Tapeout

## Abstract

> Tell us what your talk is about, in under 150 words

Over the last years it has become feasible for hobbyist hackers to design custom silicon chips,
and to get them produced for a low cost -
all using an entirely open-source Electronic Design Automation (EDA) toolchain.
We recently learned how to do this via the Tiny Tapeout project,
and was able to create custom silicon for PDM digital microphones that integrates with a microcontroller.
In this talk we will present how we designed, tested, and finally submitted our design for production.
This will also give a quick overview of the open-source EDA toolchain that make it all possible,
from Verilator for simulating the design, cocotb+Python for automated tests,
yosys+ice-storm for running on FPGA, and LibreLane for converting into something that can be manufactured.

## Keywords

chip design, EDA, open silicon

## Description

> Tell us in depth about your talk in about 500 words
> Present your key subject and how you will discuss it

At the start of this project we had never attempted to design an integrated circuit (IC), and had just barely played with FPGA.
Our goal was to submit an IC for production, and to learn it by studying openly available materials online,
and prototyping with open-source tools and low-cost ICE40 FPGA at our hackerspace.
Thanks to the Tiny Tapeout project and community it worked out!
We would like to share some of our experience with that process -
hopefully demystifying this area of hardware a bit,
and maybe inspiring others to dip their toes into FPGA and/or chip design,
and further grow this area of open source hardware community.

The chosen project was to implement support for audio input for microcontroller using a digital PDM microphone.
The Pulse Density Modulation (PDM) protocol is a 1-bit signal at several Mhz clock rate,
and requires a filter to convert into an audo waveform (PCM samples) that the microcontroller can process.
The PCM conversion is done using an hardware-efficient topology called Cascaded integrator-comb (CIC).
One version of the design runs as a standalone PDM-to-PCM converter chip, using external SPI bus to communicate with the microcontroller.
Another version is an integrated memory-mapped peripheral for the community-developed tinyQV RISC-V microcontroller.
Testing was done using a combination of simulation and using FPGA-based hardware.

Our project was submitted for the ttsky25a production run in September 2025,
and the chips are estimated to be received in May 2026.
Depending on the actual timing of the delivery, the talk may include demos or of the produced chip.

Tiny Tapeout is a project that allows anyone to send chip designs for manufacturing.
This works by pooling all the designs from different particpants into one production run,
supported by standardized setup and tooling that is shared.
Production runs happen around 4 times per year, and production typically takes around 6 months.
Cost to submit a design is under 100 EUR, and under 400 EUR for a development board with chip.
https://tinytapeout.com/

tinyQV is a RISC-V microcontroller designed especially for Tiny Tapeout.
https://github.com/MichaelBell/tinyQV

There is a comprehensive open-source EDA toolchain for IC/chip design,
made up of a number of projects that are used together to form a production flow.
Some of the key components we used are:
Verilog. Hardware Description Language, IEEE standard.
YoSys. Framework for synthesizing Verilog. https://yosyshq.net/yosys/
cocotb. Python-based test framework for register-level hardware. https://docs.cocotb.org/en/development/
Verilator. A Verilog simultor. https://verilator.org/guide/latest
LibreLane. Convert designs to ASIC manufacturing. https://librelane.readthedocs.io/en/latest/


