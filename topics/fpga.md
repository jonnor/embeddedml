
# FPGA for TinyML

Either as reconfigurable hardware, or as prototyping/testing ground for accelerators.

## Research questions

- What kind of acceleration would be beneficial in a low-power FPGA for TinyML applications?
- In which applications is an FPGA preferrable over off-the-shelf microcontroller?

## Soft CPUs for small FPGAs

CPU cores

- [picorv32](https://github.com/YosysHQ/picorv32). Support Wishbone and AXI4 Lite buses.
- [FemtoRV](https://github.com/BrunoLevy/learn-fpga/tree/master/FemtoRV). Includes simple PicoSoc
- [neorv32](https://github.com/stnolting/neorv32?tab=readme-ov-file). Includes simple SoC
- [CV32E40P](). Has sleep support. LiteX allows deploy to FPGA?

System on Chip

- [litex](https://github.com/enjoy-digital/litex). Supports RISC-V cores

## Low-power FPGA hardware

Really want something that has at least enough block RAM for the registers of soft CPU.

FPGAs

- iCE40UP5K. 128 KBit block RAM, 8 DSP blocks. QFN48 package. 8 USD @ 1k.

Development boards

- TinyVision pico-ice. iCE40UP5K. 4x PMOD
- Icebreaker. iCE40UP5K. 2x PMOD

## ICE40 for TinyML

ICE40 has 16x16 sysDSP blocks. SB_MAC16
yosys supports inferring DSP blocks for multiplications.
PicoRV supports this?
https://github.com/YosysHQ/picorv32/pull/202/files

## Existing work

#### Comparison and analysis of open-source RISC-V cores for resource-constrained FPGAs
N Morawski, 2024.
https://mrwski.eu/projects/data/riscv_ice40.pdf

Tested various RISC-V soft-CPUs on iCE40UP5K. Measured DMIPS per MHz.
PicoRV32 0.348-0.380, VexRiscV 0.505-0.668, RP2040 ARM Cortex M0+ 1.426.
Maximum frequency achieved was from 18-27 Mhz.
Minimum size was around 2000 LUTs.
Was barely able to fit RV32IM (hardware multiplier) for PicoRV32, but not RV32IF (hardware FPU).
Tested a Local Outlier Factor implementation with floating-point Euclidean distance,
combined with DSP preprocessing of 20-50 length time-series.
Found LOF to take 99% of the time.
! did not test integer/fixed-point computation as alternative to soft-float.

My conclusion.
RISC-V on ICE40 has a 50% performance disadvantage over RP2040.
And only competes at 1/10x the max performance.
Would need to be better in terms of power, or hardware acceleration.

#### ICE40 power measurements by TinyVision

https://github.com/tinyvision-ai-inc/ice40_power

Minimal functional, 10 kHz. 151uW
At 16 Mhz with a math benchmar around 2000 uW @ 1.2V.
Giving around 125 uA/Mhz, as an lower estimate.

! missing RISC-V softcore numbers. Requested at https://github.com/tinyvision-ai-inc/ice40_power/issues/1


RP2040 datasheet specifies 3000-5000 uA at 12 Mhz with both cores active.
Might be as high as 250-400 uA/Mhz.

But there are many other microcontrollers with under 100 uA/Mhz,
including chips with built-in FPU.

STM32U5 Cortex M33 claim 16.3 uA/Mhz at 3.3V with buck regulator, and around 60 uA/Mhz with LDO.

My conclusion:
ICE40 RISC-V might be similar to RP2040 in power consumption,
but likely at disadvantage over other low-power microcontrollers.

Microcontrollers have good built-in support for sleep states.
FPGA with soft-core typically only do internal clock gating, limiting power reduction.

