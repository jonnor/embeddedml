
# TODO

### Firmware

- Get BC7161 to send BLE advertisement
- Test BLE advertisement rates
Want to send 50 Hz or 25 Hz accelerometer sample data to computer and/or phone.
Try to see if one can change BLE advertisement payload as often as every 100 ms,
and still read all the advertisements on the other side. Use a sequence counter.
- Implement FIFO based reading from LIS2DH12 accelerometer on PY32. At 50 Hz

### Bringup

- Can make sound with buzzer, using PWM
- Check can communicate with accelerometer
- Read BATT_VOLTAGE
- Check BATT_CHARG
- Check BATT_PROG
- Can dim LEDs using PWM

### Demo
See toothbrush repository


# Board bringup

#### LIS2DH12 driver

https://github.com/STMicroelectronics/lis2dh12-pid?tab=readme-ov-file
https://github.com/STMicroelectronics/STMems_Standard_C_drivers/blob/master/lis2dh12_STdC/examples/lis2dh12_read_fifo.c

https://github.com/IOsetting/py32f0-template/blob/main/Examples/PY32F0xx/LL/I2C/ADXL345_3-axis_Accelerometer/main.c
https://github.com/IOsetting/py32f0-template/blob/main/Examples/PY32F0xx/LL/I2C/MPU6050_6-axis_motion/mpu6050.c

#### PWM

py32f003 has hne high freq TIM1, and 4 general (TIM3/TIM14/TIM16/TIM17), and one LPTIM.

Seems TIM1 has 4 channels. TIM3 has 3. Others just 1-2.

Can map GPIO to timer for PWM using alternate function. But only a few options for this.
Buzzer pin, PF1, is TIM14_CH1 (AF13).

Probably should use soft-PWM for LEDs.

Note that TIM1 is used for ADC for audio, where used.


#### Debugging

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


