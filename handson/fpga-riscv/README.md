
# LiteX RISC-V SoC on ICE40

**Status: Experimental**. Below is a rough collection of notes.

## Notes

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

Build, load bitstream and flash firmware
```
python -m soc.targets.muselab_icesugar --cpu-type=vexriscv --cpu-variant=minimal --build --load --flash --flash-program firefox
```

```
picocom /dev/ttyACM0 -b 115000
```

NOTE: to flash icesugar, need a tool called [icesprog](https://github.com/wuxx/icesugar/tree/master/tools/src) (NOT `iceprog`).

#### Tested CPUs

- `--cpu-type vexriscv --cpu-variant minimal`. Blink works. 4500 LUTs. No JTAG pins.
- `--cpu-type picorv32 --cpu-variant minimal`. Blink works. 3400 LUTs
- `--cpu-type femtorv --cpu-variant standard`. Blink and UART out works. 2500 LUTs. **No interrupts**.
- `--cpu-type fazyrv --cpu-variant standard`. Blink works. 2300 LUTs. **No interrupts**.
- `--cpu-type serv --cpu-variant standard`. Blink **FAILS**. Under 2000 LUTs
- `--cpu-type naxriscv --cpu-variant standard`. Unable to build? Too large for ICE40?
- `--cpu-type vexiiriscv --cpu-variant standard`. Takes 9k. Too large.
- `--cpu-type neo32rv --cpu-variant standard`. assert reset_address == 0x0000_0000. Has JTAG?

#### Zephyr on LiteX

NOTE: must have timer uptime enabled. For example by adding `--timer-uptime`.

XXX: when trying to run `minimal` Zephyr sample.
Not seeing any output on serial from the printk()

### TODO

Must

- Test PDM peripheral from TinyTapeout/galearn
- Try running some code using emlearn

Want

- Get GDB working. Via UARTBone bridge FAILED. Via JTAG using a DAPLink compatible device?
- Get MicroPython on Zephyr working
- Test simulation support in LiteX
- Test DMA for audio data transfer instead of FIFO
- Get running on Upduino V3 boards
- Do power measurements of ICE40UP5K. Static, minimal dynamic

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

### Unable to upload program via BIOS serialboot

Getting either CRC error, or unexpected response from device.
Similar to https://github.com/enjoy-digital/litex/issues/2208

### Can't extract CSR name from code in Python 3.14

https://github.com/enjoy-digital/litex/issues/2399
https://github.com/m-labs/migen/issues/297

Fixed after 0.9.2 release. But no new release as of January 2026?
https://github.com/m-labs/migen/commit/4c2ae8dfeea37f235b52acb8166f12acaaae4f7c

Have to install migen from git!


### GDB for LiteX with VexRISCV

Per https://github.com/enjoy-digital/litex/wiki/JTAG-GDB-Debugging-with-VexRiscv-CPU

python -m soc.targets.muselab_icesugar --cpu-type=vexriscv --cpu-variant=lite+debug --uart-name crossover+uartbone --uart-baudrate 115200 --build --load

litex_server --uart --uart-port=/dev/ttyACM0

shdl-riscv-openocd -c 'adapter driver dummy' \
              -c 'adapter_khz 1' \
              -c 'jtag newtap lx cpu -irlen 4' \
              -c 'target create lx.cpu0 vexriscv -endian little -chain-position lx.cpu -dbgbase 0xF00F0000' \
              -c 'vexriscv cpuConfigFile cpu0.yaml' \
              -c 'vexriscv networkProtocol etherbone' \
              -c 'init' \
              -c 'reset halt'


Not working.

```
Info : clock speed 1 kHz
Info : TAP lx.cpu does not have valid IDCODE (idcode=0x0)
Info : TAP auto0.tap does not have valid IDCODE (idcode=0x80000000)
Info : TAP auto1.tap does not have valid IDCODE (idcode=0xc0000000)
Info : TAP auto2.tap does not have valid IDCODE (idcode=0xe0000000)
Info : TAP auto3.tap does not have valid IDCODE (idcode=0xf0000000)
Info : TAP auto4.tap does not have valid IDCODE (idcode=0xf8000000)
Info : TAP auto5.tap does not have valid IDCODE (idcode=0xfc000000)
Info : TAP auto6.tap does not have valid IDCODE (idcode=0xfe000000)
Info : TAP auto7.tap does not have valid IDCODE (idcode=0xff000000)
Info : TAP auto8.tap does not have valid IDCODE (idcode=0xff800000)
Info : TAP auto9.tap does not have valid IDCODE (idcode=0xffc00000)
Info : TAP auto10.tap does not have valid IDCODE (idcode=0xffe00000)
Info : TAP auto11.tap does not have valid IDCODE (idcode=0xfff00000)
Info : TAP auto12.tap does not have valid IDCODE (idcode=0xfff80000)
Info : TAP auto13.tap does not have valid IDCODE (idcode=0xfffc0000)
Info : TAP auto14.tap does not have valid IDCODE (idcode=0xfffe0000)
Info : TAP auto15.tap does not have valid IDCODE (idcode=0xffff0000)
Info : TAP auto16.tap does not have valid IDCODE (idcode=0xffff8000)
Info : TAP auto17.tap does not have valid IDCODE (idcode=0xffffc000)
Info : TAP auto18.tap does not have valid IDCODE (idcode=0xffffe000)
Info : TAP auto19.tap does not have valid IDCODE (idcode=0xfffff000)
Warn : Unexpected idcode after end of chain: 21 0xfffff800
Error: double-check your JTAG setup (interface, speed, ...)
Error: Trying to use configured scan chain anyway...
Error: lx.cpu: IR capture error; saw 0x0f not 0x01
Warn : Bypassing JTAG setup events due to errors
```

Never gets to listening on port XXX

