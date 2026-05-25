
# Hardware

Per board

- 10x 3 pin connectors - though many need only 2
- 3x 4 pin connectors
- 1x 5 pin connector

Must-have

- Well supported chip. ESP32 or RP2
- Good WiFi-support. ESP32 vanilla/S3/C3/C6. Pico W RP2024

Want to have

- Analog sensor
- Accelerometer/IMU
- I2C extension port


### Alternatives

#### XIAO with base board?

! ESP32 wokwi is very old
Buzzer, push button
I2C extension connectors
SSD1306 OLED

#### M5StickC PLUS 2?
Out of production!!
Familiar. Grove extension. Accel. Buzzer. Button. Qwiic adapter possible. Simple PMIC.
! no microphone
! no analog sensors
Relatively costly. Already have 5+
https://www.digikey.no/no/products/detail/m5stack-technology-co-ltd/K016-P2/22015383

#### Pico W with expansion board?

! Pico only has 3 ADC pins. GPIO26,27,28

https://www.digikey.no/no/products/detail/raspberry-pi/SC0918/16608263

Expansion board
Would be nice if it maps quite nicely to Pico headers.
So that participants can see the mapping easily.
! will need to expand VCC and GND connections

https://www.digikey.no/no/products/detail/dfrobot/DFR0836/15283076
https://www.digikey.no/no/products/detail/sb-components-ltd/SKU20812/16836957?s=N4IgTCBcDaIAoEsDGB7ABAUQB4AcCGAdgM4IoFoBCKeATgCZoDicAkgPIgC6AvkA

And associated Wokwi modules?


#### Pico 2W
No Wokwi!
No sensors. No extension port.

