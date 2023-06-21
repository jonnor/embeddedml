
# Offloading

Should at least

- Filter frequencies into the voice band
- Implement dynamic/relative thresholding

Architectural options

- Microphone with built-in voice energy estimator.
Vesper VM1010, Vesper, TDK xxx
- Analog microphone with analog filter.
Threshold in software/ADC
- Analog microphone,
process using low-power co-processor

## ESP32 ADC

Is pretty bad. Non-linear, offset issues, lack of hardware offloading.
https://github.com/espressif/esp-idf/issues/164

## ESP32 I2S/PDM input

Definetely does not work in deep sleep.

Does not work in `light sleep`??
https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2s.html#power-management

https://esp32.com/viewtopic.php?t=30649

## ESP32 ULP
Ultra low power co-processor.
NOTE: ESP32-S2 also has a RISC-V coprocessor

Simple Finite State Machine.
Programmed in Assembler.
Can access ADC.
Cannot access I2S.
Can wake up main processor.
Can share memory with main processor.

https://github.com/unixbigot/arduino_ulp/blob/master/ulp_examples/ulp_adc/adc.s
Shows upper+lower threshold checking from ADC
Uses a LUT to interpret input values. Could be used for dB conversion

https://github.com/espressif/esp-idf/tree/v5.0/examples/system/ulp_fsm/ulp_adc
100 Hz mesurements, 37 uA consumption

https://github.com/boarchuz/HULP/tree/release
Collection of macros and functions to help get the most out of the
Ultra Low Power Co-Processor (ULP) on the ESP32 with legacy macro programming.

## RP2040 Pico PIO
Two sets of PIO co-processors. 4 in each "bank".
TX and RX FIFO for sharing with main processor.


https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio
