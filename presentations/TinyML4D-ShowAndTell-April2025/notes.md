
## Project links

https://github.com/jonnor/toothbrush/

https://www.hackster.io/jonnor/automatic-toothbrush-timer-45ba5c


## Takeaways

- emlearn-micropython makes TinyML easy
MicroPython means you just need to know Python
Example code for accelerometer / Human Activity Detection
Modules are implemented in C, for efficiency
- TinyML is a nice addition for makers and engineers in embedded systems toolkit.
Enable new products, new features to existing products.
- Can also use emlearn from C

## Disposition

10 minutes.
5-8 slides.

#### Intro

Image: project overview

#### Motivation
Building examples for emlearn/MicroPython.
Complete end-to-end project. Non-standard use-case.
Designing behavior. Data, training, firmware, testing it out.

#### What it does
Track how long you are actively brushing your teeth. Gives you sound cue as you progress, and complete 2 minutes.
Because brushing sufficiently long enough is important for dental health. And most people skip on it.
Design principle, be unobtrusive. You just use it, without any change, and it helps you out.

#### How it was made - hardware/firmware
M5StickC. ESP32. With built-in accelerometer and buzzer. And battery.
Firmware. MicroPython based.

Image: state diagram

Image: firmware architecture diagram
TODO, highlight the ML parts

#### How it was made - machine learning

Collected data using har_trees example from emlearn-micropython. Stores to internal FLASH.

Recorded video using mobile phone. Acts as the reference for ground thruth.
Did a "3 taps" sequence at start/end to have something to syncronize device/accelerometer and phone/video. Like the "clapper" used in film.

Labeling using Label Studio.

Training pipeline har_trees in emlearn.
Also has deployment. Splits out a trees.csv file, can be loaded in emlearn-micropython.

Image: Label Studio? training script output?

#### ? How it was made - testing

? testing on the host
emlearn-micropython is portable. Same code runs on PC.
Data pipeline is separated from I/O.
Can test entire pipeline and application logic, or synthetic data.
Only accelerometer driver and buzzer driver are excempt.

Image: Data pipeline running on PC // automated tests

#### Potential improvements
Make setup more practical.
Attach to toothbrush without needing zipties. Maybe flexible using TPU.
Should also be smaller, take up less space.
Make it cheaper.
Get it working on DollarML board. Puya PY32F0 series.
Porting to C. Using emlearn C API.
Low-power sleep mode. Periodic wake-ups.

Image: DollarML board
Image: Case prototype

#### Call to Action
Interested in making TinyML devices and applications?
Check out emlearn-micropython.

Link to documentation.

Image: project overview

