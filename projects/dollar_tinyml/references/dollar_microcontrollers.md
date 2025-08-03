
# Sub 1 dollar microcontrollers

Can get a pretty modern microcontroller for 1 USD.
Even down 0.10 USD. Some options also below this.

## Overview

Prices are per Jan 2024, according to [LCSC](https://www.lcsc.com/).

- 1x RP2040 chip. Cortex M0+
`0.80 USD @ 1k`
- JieLi Tech AC6329C4
**BLE** microcontroller. 8 kB RAM / 256 kB FLASH.
`0.30 USD @ 1k`.
- WCH CH592F. `0.48 USD @ 1k`. BLE+USB
- WCH CH571. `0.40 USD @ 1k`. BLE+USB
- WCH CH582F. `0.68 USD @ 1k`. BLE+USB
- CH32V203. 64 kB RAM / 256 kB. USB. 0.35 USD @ 1k.
- CH32X035. 64 kB RAM / 256 kB. USB. OPA/PGA. 0.25 USD @ 1k.
- ATTiny with 4KB FLASH / 512 bytes RAM
`0.4 USD @ 1k`
- STM32G030F6P6 0.30 USD 32 kB FLASH / 8 kB RAM.
0.2 mA in LPRUN 2Mhz
5 uA in STOP 1 no SRAM retention with RTC.
`0.30 USD @ 1k`
- WHC CH552. 8-bit. 1kB RAM. USB. `0.28 USD @ 1 k`.
- WCH CH32V003. RISC-V
16KB FLASH / 2KB RAM.  48MHz QFN-20
`0.15 USD @ 1k`
- WCH CH32V006. RISC-V. 8 kB RAM. 48 Khz.
`0.13 USD @ 1k`
- PY32F003. Cortex M0+
`0.15 USD @ 1k`
64 Kb FLASH / 8 kB RAM. 24 Mhz. DMA
- PY32F002. Cortex M0+
`0.10 USD @ 1k`
20 Kb FLASH / 3 kB RAM. 24 Mhz
- Padauk PFS154
`0.06 USD @ 1k`
2 kB FLASH / 128 bytes of RAM
- Fremont Micro Devices FMD FT60F011A-RB
`0.06 USD @ 1k`.
- Padauk PMS150C
`0.03 USD @ 1k`
1 kB OTP / 64 bytes of RAM. **One-time-Programmable**

## Implications for dollar TinyML

If we budget 10-20 cents USD to the microcontroller,
then we get around:

- 16-20 kB FLASH
- 2-3 kB RAM
- 24-48 Mhz clock speed
- 32 bit CPU
- No floating-point unit (FPU)

## Resources

Review of 3 cent MCUs
https://cpldcpu.wordpress.com/2019/08/12/the-terrible-3-cent-mcu/

## Candidates

### WCH CH32V003

Ch32v003 with Microphone Module and Telemetry Viewer
https://www.youtube.com/watch?v=AnvOQRSDUao

CH32V003 USB support
https://github.com/cnlohr/rv003usb
https://www.youtube.com/watch?v=j-QazXghkLY

2kB RAM. 48 MHz frequency.
Enough for soundlevel computations.
Is it enough for FFT?

CH32V003A4M6 is SOP14

RUN VDD=3.3V internal RC
FHCLK = 48MHz   6.57  4.16 mA
FHCLK = 750KHz  1.11  

SLEEP VDD=5.0V internal RC
FHCLK = 750KHz 0.47 0.43 mA

Sleep wakeup    30 us
Standby wakeup  200 us

ADC sample rate up to 430 kHz

2 opamp inputs, 1 output. 1 single/differential opamp.

KiCAD symbols
https://github.com/sad-electronics/wch-kicad-lbr
https://github.com/Taoyukai/wch_kicad_library

Flashing tools for low-cost microcontrollers. Implemented in pure Python
https://github.com/wagiminator/MCU-Flash-Tools

## WCH CH32V006

Like CH32V003 but with more RAM, FLASH and pins.

CH32V005 is same, but no TouchKey support or TIM3. Missing OPA polling.
CH32V005 is same, but tailored for motor control. High voltage ADC, 3 channels.

Integrated opamp is very interesting for audio type applications.
Har programmable gain, and comparator.
DMA.
ADC is just 12 bits. But PGA should make it possible to get much more out of it compared to static gain.

- Gain Bandwidth product. 64 Mhz. Super
- Equivalent noise leve. 60 - 100 nV/sqrt(Hz) @ 1 Khz. Not so good... Want 20 nV at 10 Khz
- Slew rate. 10 V/us. Super, way above 0.25 needed
- Current consumption. 1.4 mA. Not great. Around 5-10x external competitors

Might get better noise figures by having a common-emitter first stage?
Goal would be to add 10-100x gain with that, to bring up the signal a bit.
Like a BC849C.

CH32V006F8U6 available at LCSC. QFN-20 pin. 18 gpio.

Has Zephyr support!
https://docs.zephyrproject.org/latest/boards/wch/ch32v006evt/doc/index.html

CH32V005D6U6 is QFN-12. `0.10 USD @ 1k`. 32 kB FLASH, 6 kB RAM.

## Puya PY32F0

PY32F002A/003/030 considered very similar.

- PY32F002A 3 KB RAM / 20 KB FLASH / 24 MHz. 0.09 USD @ 1k
- PY32F030. Multiple variants. 2-8 KB RAM, 16-64 KB FLASH
- PY32F003. Multiple variants. 2-8 KB RAM, 16-64 KB FLASH

LCSC has PY32F003x6, 4 kB RAM / 32 kB FLASH.
PY32F003W16S6TU SOP16, 0.13 USD @ 1k.

Meet Puya PY32 – The 8-cent Arm Cortex-M0+ microcontroller
https://www.cnx-software.com/2023/02/09/8-cents-for-an-arm-cortex-m0-microcontroller-meet-puya-py32-series-mcus/

EEVBLOG thread on Puya PY32
https://www.eevblog.com/forum/microcontrollers/$0-11-py32f002a-m0-24mhz-320kb-actually-324kb-more-peripherals/

English datasheets here
https://github.com/IOsetting/py32f0-template/wiki

Open source toolchain here
https://github.com/IOsetting/py32f0-template/
Based on STM32HAL, GCC, JLINK

PY32F003F16U6.

### Padauk

https://github.com/free-pdk

SDCC C compiler. For tiny/old/odd 8 bit targets
https://sdcc.sourceforge.net/


### AC6329C4

Under 0.30 USD. Incredibly cheap.
Available from LCSC, https://www.lcsc.com/products/Microcontroller-Units-MCUs-MPUs-SOCs_11329.html?keyword=AC6329C4

Bluetooth 5.x support.
USB OTG support.
Integrated Li-ion changer.
73 kB RAM??
RISC-V MCU?
96 Mhz clock.
PMU with power saving.

Open SDK here: https://github.com/Jieli-Tech/fw-AC63_BT_SDK

Documentation primarily in Chinese. Only a little bit in English.

### Storage

SPI NOR FLASH

- xx 25Q16   2 MB   `0.09 USD @ 1k`
- xx 25Q8    1 MB   `0.08 USD @ 1k`
- xx 25WD20  256 kB `0.05 @ 1k`

SOIC8 or USON8. Or WSON8

https://docs.zephyrproject.org/latest/build/dts/api/bindings/mtd/jedec%2Cspi-nor.html

