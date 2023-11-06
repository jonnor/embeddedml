
RTX3090. Approx 1000 USD

What can one get for 1 USD?
Assuming 1k volumes.

#### Microcontroller

Can get a pretty modern microcontroller.

- 1x RP2040 chip. Cortex M0+
`1 USD @ 1k`
- ATTiny with 4KB FLASH / 512 bytes RAM
`0.4 USD @ 1k`
- STM32G030F6P6 0.30 USD 32 kB FLASH / 8 kB RAM.
With USB!
0.2 mA in LPRUN 2Mhz
5 uA in STOP 1 no SRAM retention with RTC.
`0.30 USD @ 1k`
- CH32V003. RISC-V
16KB FLASH / 2KB RAM.  48MHz QFN-20
`0.15 USD @ 1k`
- PY32F002. Cortex M0+
`0.10 USD @ 1k`
20 Kb FLASH / 3 kB RAM. 24 Mhz


Flashing tools for low-cost microcontrollers. Implemented in pure Python
https://github.com/wagiminator/MCU-Flash-Tools

### Sensors
Prices from JLCPCB

- MEMS microphones `<0.2 USD`
- Photointerruptor 0.1 USD
- LIS2DH12TR accelerometer. 0.3 USD

### Power

Consumable battery

- CR1216 battery at 0.2 USD
- CR2477 `0.8 USD @ 1k`

Rechargable battery

- LIR1220 `0.2 USD @ 1k`. 7 mAh
- Battery charger `0.06 USD @ 1k`
 

### Connectivity

#### Holtek BC7161
BLE beacon IC
`0.2 USD @ 1k`. 
SO8 package
https://www.holtek.com/productdetail/-/vg/BC7161
Communication over I2C

Holtek BC7262
SO10 package
Communication over I2C


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


- MCU. PY32F002 . `0.10 USD @ 1k`
- Microphone. LinkMems `0.10 @ 1k`
- BLE. Holtek BC7161 `0.20 @ 1k`
- Analog opamp. `0.10 @ 1k`
- Power. USB edge connector?

Also very constrained for audio with 2 kB RAM.
Probably will use 1-10 mA, for continious listening.
Just 1 hour or so on battery?

But if one can put it in a USB socket somewhere, can do continious monitoring.

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





