
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

## Weight measurement

Strain gauge BF350-3AA, 0.30 USD @ 100 pcs
Need a Weatstone bridge and opamp for signal conditioning.
Plus needs to be attached to an elastic bar that experiences strain.
Can probably be FR4 PCB structure.

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




