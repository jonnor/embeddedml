
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

## LiteX

### Can't extract CSR name from code in Python 3.14

https://github.com/enjoy-digital/litex/issues/2399

