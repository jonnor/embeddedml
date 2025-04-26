
# TODO

Motion dollarML

- Board bringup of dml20m
- Port toothbrush application to C/dml20m.
LIS2DH driver, buzzer PWM, statistical features computation.
https://github.com/jonnor/toothbrush/ 
- dml2Xm. Switch to USB-C connector. Debug behind USB conn?
On-board 5050 SMD buzzer (optional)?
Move BM7161 module to back, optional? Maybe capacitive touch?

Audio dollarML

- Design a dml2Xa board. Only with microphone.
Maybe switch to USB-C. Maybe make Holtek optional.
- Prototype/test audio preprocessing. Mel spectrogram (CMSIS+emlearn) and IIR filterbank (libvfad).
- Finish post on audio preprocessing.
- Create post on Sound Event Detection with Recurrent Neural Networks

Common

- Add a link to the main README in embeddedml
- Make mockup/concept sketch/image for use as wristband
- Get Holtek BLE PoC working
- Create post on holbeacon C library


### Hardware

See [./hardware/dml10/worklog.md](./hardware/dml10/worklog.md)
and [./hardware/dml20m/worklog.md](./hardware/dml10/worklog.md)

# DONE

- dml20m. New board for motion/accelerometer, sent to production.
- Initial research on microcontrollers,
- Theoretical check that RNN can fit into 2 kB RAM / 32 kB FLASH.
Confirmed. FastGRNN etc.
- Theoretical check that RF for HAR can fit into 2kB RAM / 32 kB FLASH
- Hyperparameter tuning RF for small size, for HAR on PAMAP2 dataset
- Post on HAR+RF feasibility
- Check approximate dimensions for board. Currently 52x26mm incl USB connector, 40x26mm excluding
- Create 1 or 2 project images
- dml10. Hardware ordered
- dml10. Hardware initial bringup done.
- Make mockup/concept sketch/image for use as sound sensor. With USB PSU?
- Tested TinyMaix CNN on device.
