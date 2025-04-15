#!/bin/bash -xe

# Compile the code
arm-none-eabi-gcc -mcpu=cortex-m3 -mthumb -g -O0 -Wall -c test_peripheral.c -o test_peripheral.o
arm-none-eabi-gcc -mcpu=cortex-m3 -mthumb -g -O0 -Wall -c startup.c -o startup.o

# Link the objects
arm-none-eabi-gcc -mcpu=cortex-m3 -mthumb -g -O0 -T linker.ld -nostartfiles -Wl,-Map=firmware.map test_peripheral.o startup.o -o firmware.elf

# Create binary format if needed
arm-none-eabi-objcopy -O binary firmware.elf firmware.bin

qemu-system-arm -M mps2-an385 -cpu cortex-m3 -kernel firmware.elf -nographic -semihosting -S -gdb tcp::1234

#qemu-system-arm -M mps2-an385 -cpu cortex-m3 -kernel firmware.elf -monitor none -serial stdio -S -gdb tcp::1234


