
### System-view

Could one build an entire application?
Challenge: Power, communication


#### A health wristband
With Human Activity Recognition and pulse monitoring.
Logging to internal FLASH, USB connectivity.

- XySemi XC5011 charger
- Everlight Elec ITR8307/S17/TR8(B)
- STMicroelectronics STM32G030F6P6
- STMicroelectronics LIS2DH12TR
- LIR1220 battery

Total BOM: `< 1.0 USD @ 1k`

7 mAh / 24 hour = 0.29 mA average consumption.
7 mAh / 30 days = 9 uA average consumption.

32 kB FLASH / 8 kB RAM.

16 kB / 4 kB for model.
1 second @ 50 Hz triax = 0.3 kB

32-slot data FIFO. Only need wakeup couple of times per second

#### Smart audio

- MCU. CH32V003. `0.13 USD @ 1k`
- Microphone. LinkMems `0.10 @ 1k`
- BLE. Holtek BC7161 `0.20 @ 1k`
- Analog opamp. `0.10 @ 1k`. Maybe not needed?? With CH32V003
- Power. LIR1220?. Edge USB connector?

Also very constrained for audio with 2 kB RAM.
Probably will use 1-10 mA, for continious listening.
Just 1 hour or so on battery?

But if one can put it in a USB socket somewhere, can do continious monitoring.


### Activity tracker

Requirements

- Way to indicate activity. Couple of buttons?
- Way to give user feedback on activity detected and. RGB controllable LEDs
- Way to measure motion. Accelerometer. LIS2DH12
- Possible to charge. Charger. USB Type PCB connector?
- Battery powered for some hours. LIR1220 or LIR1025
- Small size. Easy to place. Maximum 40x45 mm? Prefer 20x35mm
- Microcontroller. Puya PY32 is familiar. PY32F003F18U6TR 8kB SRAM, QFN-20.
- Optional connectivity to phone. BLE, Holtek BM7161? Maybe put on back

Micro. 15 cents
Accel. 25 cents
BLE. 20 cents
Battery. 25 cents
= 85 cents

## Weight measurement

Strain gauge BF350-3AA, 0.30 USD @ 100 pcs
Need a Weatstone bridge and opamp for signal conditioning.
Plus needs to be attached to an elastic bar that experiences strain.

Strain gauge can probably be done as PCB structure on FR4.
https://github.com/vapetrov/PCB_strain_gauge?tab=readme-ov-file
Got very good results.
Using traces on a 20x100 mm PCB.
4-element sensing bridge.
! note, had to use a high current. Nearly 100 mA

Used 2512 SMD resistors on PCB to measure force.
Used as an end-stop / height measuring for 3d printer.
https://github.com/IvDm/Z-probe-on-smd-resistors-2512

Tested first a classic cantilevered rectangle.
Then designed a custom mount for the hotend.

> One way to possibly get additional sensitivity from this design would be to rout a thin slot in the PCB directly underneath each resistor.
> The slots would slightly weaken that area of the PCB, concentrating the flexing there instead of distributing it across the entire arm.
https://hackaday.com/2019/01/27/quartet-of-smd-resistors-used-to-sense-z-axis-height/

HX711 25 cents in 1k volumes.

Could be used for a kitchen scale?
At least giving out empty to full rating. In say 10 increments? Or percentage.
May need temperature compensation.
May need linearity compensaton.
Should have a tare for empty, 0%.
And a "tare" for full, 100%.

Good article on mounting strain gauges
https://www.iqsdirectory.com/articles/load-cell/strain-gauge.html
Bending half bridge seems most relevant

#### IoT sensor
BLE beacon

#### NRF52 with accelerometer
HolyIoT or similar.
7 USD @ 1
5 USD @ 1k

Not yet 1 USD. But `<< 10 USD`.

Sensors 100x 7 = 700
IoT gateway. 100 USD.

Conclusion:
One can get system with 100 ML-enabled sensors for price of 1 RTX3090

But 16 kB RAM and 192 kB FLASH.
How to run ML on this?
And what is feasible vs infeasible?




