
# RISC-V softcore on ICE40


## neo32rv

On Arch Linux, needed to install from AUR

    python-pytooling 8.11.0-1
    ghdl-yosys-plugin-git
    riscv-none-elf-gcc-bin

Needed to specify the ghdl plugin

    make BOARD=UPDuino-v3.0 MinimalBoot YOSYS='yosys -m ghdl'

TX/RX is on pin 28/38 on UPDuino 3.1. Default baudrate is 19200

    picocom /dev/ttyUSB0 -b 19200

For the software, one try to can upload via built-in bootloader

    make upload UART_TTY=/dev/ttyUSB0

    !! currently not working

TODO: try to use program baked into bitstream instead
TODO: try on iceSugar instead

## LiteX


### LiteX on IceSugar 1.5

Setup virtualenv with supported Python version
```
python3.12 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip install -r requirements-litex.txt
```

Build, load bitstream and flash BIOS software
```
python -m litex_boards.targets.muselab_icesugar     --cpu-type=vexriscv     --cpu-variant=minimal     --build --load --flash
```

```
picocom /dev/ttyACM0 -b 115000
```

NOTE: to flash icesugar, need a tool called [icesprog](https://github.com/wuxx/icesugar/tree/master/tools/src) (NOT `iceprog`).

### TODO

Must

- Get GDB working. Via UARTBone bridge?
- Create a custom peripheral, test read/write from software
- Try integrating the PDM peripheral from TinyTapeout/galearn
- Try running some code using emlearn

Want

- Automatic build of the firmware
- Test a smaller CPU.
serv did not work on first try. PicoRV32? femtorv? neorv32? fazyrv?
- Get Zephyr-based firmware running
- Get UART from firmware to work
- Try out the simulation support

### References

[Getting started with Litex on a Tang Nano 9K](https://justanotherelectronicsblog.com/?p=1263)

Tutorial/walkthrough of SoC setup and custom peripheral (PWM).
Also discusses how to make a program and upload it.
python -m litex.tools.litex_term /dev/ttyACM0 --kernel foo.bin


https://wot.lv/from-zero-to-soc-in-litex.html

Says LiteX BIOS should print stuff on UART on boot.


### LiteX on Upduino v3.x

https://github.com/tinyvision-ai-inc/UPduino-v3.0/issues/16

https://github.com/Xenador77/litex-boards/blob/master/litex_boards/targets/upduino_v3.py


### Can't extract CSR name from code in Python 3.14

https://github.com/enjoy-digital/litex/issues/2399
https://github.com/m-labs/migen/issues/297

Fixed after 0.9.2 release. But no new release as of January 2026?
https://github.com/m-labs/migen/commit/4c2ae8dfeea37f235b52acb8166f12acaaae4f7c

Same in Python 3.12
With Python 3.10, I get litex 2024.12 and migen 0.9.2 - old
