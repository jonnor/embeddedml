
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

