
# TODO

Next PCB

- Move LIR battery to board surface, instead of on top of components.
PCB needs to be longer, maybe 45 mm.
Should reduce from 5mm height to 3.5 (USB-C+PCB dictates).
- Maybe put Holtek BLE chip as optional
- Maybe switch to USB-C connector.

Bringup

- Can make sound with buzzer, using PWM
- Check can communicate with accelerometer
- Can dim LEDs using PWM

Demo. See toothbrush repository

# Board bringup

##### Debugging

make gdb
arm-none-eabi-gdb -ex 'file Build/app.elf'  -ex 'target remote :3333'

!! make flash does not build. Must run make first...

#### 2025-04-26

Changed MCU_TYPE to PY32F003x8.

Get 3.3v when powering USB with 4.5V. OK.

Can program board via DAPLink on the TagConnect. OK

Can blink all LEDs. Red,green,blue. OK.

Can read button. OK

When running from USB power without battery connected.
Starts in 2-3 seconds. Runs for some seconds, then shuts off.
Contincues in this cycle.
OK, but means battery must always be present.

At 5.0V VBUS, with LED on green max, VBAT 4.15 and increasing.
Also with LED on white max.
Looks to charge. OK

At 4.5V VBUS, with LED on green max, VBAT 3.8V and slight decreate.
Struggles to charge?

! Tried getting serial output via DAPLink. No output?


