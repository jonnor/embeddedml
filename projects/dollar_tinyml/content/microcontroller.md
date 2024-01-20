
If the complete BOM for sensor is to be under 1 USD,
the microcontroller needs to be way below this.
Preferably below 25% in order to leave budget for sensors, power and communication.

Thankfully there has been a lot of improvements in this area over the last years.

Looking at LCSC.com in we can find some interesting candidates.

- ST STM32G030F6P6. 32 kB FLASH / 8 kB RAM. `0.30 USD @ 1k`
- WCH CH32V003. RISC-V. 16KB FLASH / 2KB RAM.  48MHz QFN-20. `0.15 USD @ 1k`
- PY32F003x6. 4 kB RAM / 32 kB FLASH. `0.13 USD @ 1k`.
- PY32F002. Cortex M0+. 20 Kb FLASH / 3 kB RAM. 24 Mhz `0.10 USD @ 1k`
- Padauk PFS154. 2 kB FLASH / 128 bytes of RAM, `0.06 USD @ 1k`
- Fremont Micro Devices FMD FT60F011A-RB. 1kB FLASH / 64 bytes RAM. `0.06 USD @ 1k`.

There are also a very few sub-1 USD microcontrollers that have integrated connectivity.

- WCH CH582F. Bluetooth Low Energy. `0.68 USD @ 1k` 

## Implications for 1 dollar TinyML project

It looks like if we budget 10-20 cents USD to the microcontroller, then we get around:

- 16-20 kB FLASH
- 2-3 kB RAM
- 24-48 Mhz clock speed
- 32 bit CPU
- No floating-point unit (FPU)

At this price point the WCH CH32V003 or the Puya PY32F003x6 look like the most attractive options.
Both have decent support in the open community.
WCH CH32 can be targetted with [ch32v003fun](https://github.com/cnlohr/ch32v003fun),
and Puya with [py32f0-template](https://github.com/IOsetting/py32f0-template).

What kind of ML tasks can we manage to perform on such a small CPU?
