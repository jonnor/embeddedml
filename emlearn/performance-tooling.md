
## Model costs 
The model has a cost in terms of

- Execution time
- RAM memory
- FLASH program memory
- Energy

In addition to the model there is also
- Data aquisition
- Feature extraction

Measuring energy requires external tools.

Execution time is device dependent.
And data dependent for some methods, like decision trees.
RAM,FLASH is not device dependent.

Tools for getting these values easily would be valuable
On host should be able to get RAM,FLASH very close to what will be on device.
Might have some slight compiler differences.

Execution time will be quite different.
But maybe relative speeds are quite similar?
At least within a single model type.
Differences in processor architecture might change things though.

Very practical if pretty cost metrics can be acheived without going on device.
Easier experimentation.
Can provide standard tools.
And can be integrated into automated workflows.


Could compile it for a representative device (ARM Cortex M or similar).
Can then use arm-none-eabi-size to get the FLASH and SRAM size.
Need a (device-specific) linker script to do this.

Could also use an emulator to run it, to get approximate runtimes.

### Capacity modelling tools

Purpose: Check if a proposed model fits within contraints.
Model storage, memory usage, inference time, CPU "utilization"
Allow to declare budgets, function for checking if over?

Device benchmark:

eml_bench_device

    multiply_adds/second,
    convolutions_3x3/second
    node_evaluations/second (trees)
    ffts/second (melspec)

    Average, standard deviation, 75%, 95%

Ran for each supported hardware. Publish numbers

Perf modelling.
 
    takes perf constants from benchmark
    + ML model 
    => estimate model size, mem use, inference time 

Model benchmark

    Test the real model.
    Verify against Perf model.
    Do this for a set of example models, publish numbers



# Microcontroller emulators

Would be great to have a simple way to run "inside" a microcontroller,
without needing real hardware.
Is only simple if the installation/setup of the tools are simple, though.
Could also be used for Continious Integration.

### ARM Cortex M
Mainline Qemu only support TI Stellaris lsm3s for ARM
https://wiki.qemu.org/Documentation/Platforms/ARM
Zephyr has support for this platform
https://docs.zephyrproject.org/2.6.0/boards/arm/qemu_cortex_m3/doc/index.html

Zephyr still working on Cortex M4F Qemu, using netduinoplus2
https://github.com/zephyrproject-rtos/zephyr/issues/22870

Zephyr also use QEMU for Cortex M33 hardfp, using MPS2 AN521
https://github.com/zephyrproject-rtos/zephyr/pull/35381
https://docs.zephyrproject.org/2.6.0/boards/arm/mps2_an521/doc/index.html?highlight=an521

Since qemu 4.2.0 with the insn plugin, it is possible to count the number of instructions
https://stackoverflow.com/questions/58766571/how-to-count-the-number-of-guest-instructions-qemu-executed-from-the-beginning-t
https://qemu.readthedocs.io/en/latest/devel/tcg-icount.html

mps2-an505 	arm 	cortex-m33
musca-a 	arm 	cortex-m33

Hello World tutorial
https://balau82.wordpress.com/2011/09/03/using-codesourcery-bare-metal-toolchain-for-cortex-m3/
This is however a ARM Cortex M3 chip, without floating-point support

https://github.com/ajblane/armv8m-hello

### ESP32

Qemu support for ESP32 is in a fork by Espressif, with goal of mainlining
https://github.com/espressif/qemu/wiki
As of December 2021 the patchset is only 25 patches

### AVR8
AVR is supported in qemu, including "uno" and "mega2560" machines
https://qemu.readthedocs.io/en/latest/system/target-avr.html
Also really simple to compile, as linker scripts are included with avr-gcc
https://github.com/jarijokinen/avr-examples
https://yeah.nah.nz/embedded/qemu-avr/

## Renode

Renode supports many microcontroller boards
https://renode.readthedocs.io/en/latest/introduction/supported-boards.html

Has Python APIs. Both for interacting on the outside, like over UART or poking memory,
or to implement custom pheripherals.
https://renode.readthedocs.io/en/latest/basic/using-python.html

RIOT supports both QEMU and Renode, https://doc.riot-os.org/emulators.html


