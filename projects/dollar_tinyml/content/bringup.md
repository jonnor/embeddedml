
First prototype boards arrived this week.
In the weekend I did basic tests of all the subsystems.

- Charger/regulator. Voltage levels
- Microphone+amp. Gain
- Microcontroller. Flashing, toggle GPIO pin 
- BLE module. I2C communication.
- Accelerometer. I2C communication
- LEDs. Blink

As always with a first revision, there are some issues here and there.
But thankfully all of them have usable workarounds. So we can develop with this board.

Examples of issues identified

- LEDs are mounted the wrong way. Flip them or use external pins on header
- Battery charger 4.2v is too high for BLE module and MEMS mic. Use external 3.3v regulator
- MEMS mic did not work. Use external elecret mic

Next step will be to write some more firmware to validate more in detail that the board works.
This includes:

* Driver for Holtek BC7161 BLE module (I2C)
* Driver for ST LIS3DH accelerometer (I2C)
* ADC readout for audio
