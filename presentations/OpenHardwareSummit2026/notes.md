
# Digital audio for open silicon with Tiny Tapeout


https://tinytapeout.com/chips/ttsky25a/

> Estimated delivery date 2026-05-12 (estimate as of December 2025)

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

chip design, EDA

## Description

> Tell us in depth about your talk in about 500 words
> Present your key subject and how you will discuss it

At the start of this project we had never attempted to design an integrated circuit (IC), and had just barely played with FPGA.
Our goal was to submit an IC for production, and to learn it by studying openly available materials online,
and hacking
Thanks to the Tiny Tapeout project and community.
We would like to share some of our experience with that process -
hopefully demystifying this area of hardware a bit,
and maybe inspiring others to dip their toes into FPGA and/or chip design,
and further grow this area of open source hardware community.

The project was to implement support for digital audio input for microcontroller using a digital PDM microphone.
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



## Takeaways

- Full open-source EDA pipeline. Both for silicon and FPGA
- TinyTapeout makes it possible to tape out a design for 400 EUR
- Possible for hackers/makers/engineers to learn over a few weeks/months
- Digital audio input is a bit niche in open.
- Project implements support for PDM microphones
- Design verification in simulation done using Verilator/cocotb, mostly Python, some C++
- Design verification on hardware done using ICE40 FPGA



## Looking for

-- ASYNC TALKS - 15 minute talks uploaded to the OSHWA YouTube Channel

We are especially looking for speakers who can offer insights on the current climate of Open Hardware.

Some suggested areas of interest are:

- Outer space exploration and Earth observation
- Manufacturing processes and supply chains **bit**
- Open Science, nature, or biology
- Craftwork
- Untold histories
- Speculative futures & experimental tech
- Art and design in Open Hardware
- Community engagement
- Process and iteration
- Medical devices and manufacturing



## Acknowledgements

Soundsensing
EARONEDGE project



# Notes

## Open EDA tools

open EDA tools (Yosys, OpenROAD)

Librelane (previously OpenLane) toolchain for hardening to silicon.


## Process details - 130 nm

Open PDKs for several manufacturers. Skywater, IHP, GlobalFoundry

Typically 130nm
https://en.wikipedia.org/wiki/130_nm_process

State-of-the-art for CPUs around 2002-2003.
Athlon XP Thoroughbred/Thorton/Barton
Intel Pentium M Banias
Intel Pentium 4 Northwood

STM32F103 "blue pill". ARM Cortex-M3. Up to 72 Mhz, 96 kB RAM, 1024 kB FLASH
Released in 2007.

Tiny Tapeout max frequency 66 Mhz.

https://zeptobars.com/en/read/GD32F103CBT6-mcm-serial-flash-Giga-Devices
GD32F103CBT6, clone of STM32F103
Die size 2889x3039 µm. Including SRAM.
Seprate die for FLASH.  1565x1378 µm.

https://zeptobars.com/en/read/STM32F100C4T6B
STM32F100C4T6B - is the smallest made by STMicroelectronics based on ARM Cortex-M3 core.
Die size - 2854x3123µm.

https://zeptobars.com/en/read/STM-STM32F103VGT6
STM32F103VGT6 is one of the largest STMicroelectronics's Cortex-M3 microcontrollers.
1Mb of flash and 96kb of SRAM consumes most of it's enormous 5339x5188 µm die.
180nm SRAM.

https://zeptobars.com/en/read/wch-ch32v003-risc-v-riscv-microcontroller-10-cent

Looking inside an open source ASIC with Zeptobars! - TinyTapeout
https://www.youtube.com/watch?v=zUv6sdxOaFE




GD32VF103 is a STM32F103 "clone" with RISC-V instead of ARM.
Ffeatures a 32-bit rv32imac RISC-V "Bumblebee Core" @ 108 MHz with 128KB Flash and 32KB SRAM 
https://www.cnx-software.com/2019/08/23/gigadevice-gd32v-risc-v-mcu-development-board/
RISC-V microcontroller delivers 15% performance improvement in Coremark over the company
GD32 Arm Cortex-M3 microcontroller (360 vs 312), as well as 25 to 50% lower power consumption.

Basilisk is an end-to-end open source Linux-capable SoC targeting IHP's 130nm BiCMOS Open Source PDK. It is based on our Linux-capable toolkit called Cheshire. Basilisk is part of the PULP (Parallel Ultra-Low-Power) platform.
https://github.com/pulp-platform/cheshire-ihp130-o

RISCY / 

https://docs.siliconcompiler.com/en/latest/user_guide/tutorials/picorv32_ram.html
Tutorial for making a PicoRV32 with 2kB SRAM for Skywater

wafer.space GF180MCU Run 1.
3.88 mm × 5.07 mm die area, totaling 19.67 mm². Replicated 1,000 times.

Total TinyTapeout die is 18 mm2.


SKY130 ROM: Tiny Tapeout 09 test !
https://www.youtube.com/watch?v=VtRiqPIj-dA
Biggest are 4 kB ROM blocks

## Open source FPGA

https://github.com/mole99/panamax
Taping out on Cadance MPW

Generated using Fabolous FPGA framework
https://fabulous.readthedocs.io/en/latest/index.html

Has MAC, SRAM, BRAM, REG blocks.
Also has ADC and DAC.

Master thesis.


### Tiliqua FPGA audio DSP

https://github.com/apfaudio/tiliqua
FPGA: Lattice LFE5U-25F-6BG256
4 in, 4 out
USB audio support

Made with Amaranth HDL, a Python based HDL
https://amaranth-lang.org/docs/amaranth/latest/intro.html

A Python toolbox for building complex digital hardware
https://github.com/m-labs/migen

## Open microcontrollers that have taped out

https://github.com/aesc-silicon/elemrv
Tailored to use with the IHP Open SG13G2 PDK.
Based on VexRiscV

Caravel test hardness on TinyTapeout contains a RISC-V microcontroller, incl SRAM.
Based on PicoRV32.
https://github.com/bol-edu/caravel-soc

PULPino

## SoCs and SoC framewors/builders

Do any of the common SoCs have PDM decoding?

PicoSoC has PDM generator, but not decoder?
https://lawrie.github.io/blackicemxbook/PicoSoC/PicoSoC.html

Missing PDM input

- NeoRV32. No I2S or PDM
https://github.com/stnolting/neorv32
- LiteX - has I2S, but no PDM
- OpenTitan Earl Gray. No I2S or PDM https://opentitan.org/book/hw/top_earlgrey/doc/specification.html

https://github.com/fusesoc/fusesoc-cores/

- FuseSoC. No core with I2S or PDM?
- PicoSoc. No I2S or PDM

Has PDM support

- Pulpissimo
https://github.com/pulp-platform/pulpissimo
I2S peripheral has PDM mode. I2S_PDM_SETUP in datasheet
Supports PDM_DECIMATION and PDM_SHIFT
Use either RI5CY or Ibex cores

## Other prior art wrt PDM audio input


https://github.com/kamejoko80/litex-pdm2pcm

https://github.com/antmicro/litex-vexriscv-i2s-demo
I2S core written completely in Migen, which can be connected to the LiteX SoC
I2S Zephyr driver that allows collecting and transmitting sound samples

## Digital microphones

Protocols. I2S, TDM, PDM


## Automated testing
Verilog


### Tiny Tapeout
https://tinytapeout.com

https://tinytapeout.com/chips/ttsky25a/tt_um_jonnor_pdm_microphone

TinyQV

https://tinytapeout.com/chips/ttsky25a/tt_um_tt_tinyQV

Costs approx 400 EUR to get hardware.
Under 100 EUR to get design included, without own board



