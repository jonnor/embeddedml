
# Sub 1 dollar microcontrollers

Can get a pretty modern microcontroller for 1 USD.
Even down 0.10 USD. Some options also below this.

## Overview

Prices are per Jan 2024, according to [LCSC](https://www.lcsc.com/).

- 1x RP2040 chip. Cortex M0+
`0.80 USD @ 1k`
- WCH CH582F
`0.68 USD @ 1k`.
**BLE** microcontroller
- ATTiny with 4KB FLASH / 512 bytes RAM
`0.4 USD @ 1k`
- STM32G030F6P6 0.30 USD 32 kB FLASH / 8 kB RAM.
With USB!
0.2 mA in LPRUN 2Mhz
5 uA in STOP 1 no SRAM retention with RTC.
`0.30 USD @ 1k`
- WCH CH32V003. RISC-V
16KB FLASH / 2KB RAM.  48MHz QFN-20
`0.15 USD @ 1k`
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


## WCH CH32V003

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

https://github.com/sad-electronics/wch-kicad-lbr

Flashing tools for low-cost microcontrollers. Implemented in pure Python
https://github.com/wagiminator/MCU-Flash-Tools

### Padauk

https://github.com/free-pdk

SDCC C compiler. For tiny/old/odd 8 bit targets
https://sdcc.sourceforge.net/

