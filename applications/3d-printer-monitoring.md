
# 3d-printer monitoring

Consumer grade machines should just work, be safe in operation and guide user to do the right thing.
Also very price sensitive and mostly sold as a standalone appliance, makes microcontrollers attractive.

Possible sensors:

* Accelerometer. On toolhead / bed
* High-speed current sensing of motors
* Microphone
* Should one have tachometer on fan(s), so one can eliminate them more easily?
* Camera

### Function

that can be implemented with sensors and machine learning

Detect malfuctions

* Print loose from bed, printing into thin air
* Warping, print lifts up on one side and starts pushing more on part
* Bottom layer too close to bed, usually leaves.
* Oozing or other source has left blob in model.
* Other unexpected obstruction of the toolhead, like a human hand
* Skipped steps

Detect wear/maintenance need

* Insufficient lubrication of linear bearings
* Timing belt slop/backlash. Might need to know the gcode/pathplanning
* Fan bearings worn out. Usually vibrates more and makes noise

Cost saving

* Sensors can maybe replace need for physical endstops for XY.
Already done with Trinamic stepper motor drivers.
* Sensors can maybe be used for probing Z level/bed

### Related works

Camera-based monitoring.

[Klipper Resonance Compensation using accelerometer](https://www.klipper3d.org/Measuring_Resonances.html).
Uses ADXL345 accelerometer mounted on printer head.
Can additionally have accelerometer on moving bed.
Also supports MPU-9250/MPU-9255/MPU-6515/MPU-6050/MPU-6500.
Same could be used for Condition Monitoring.
Klipper can also save the raw accelerometer data, as CSV files.
