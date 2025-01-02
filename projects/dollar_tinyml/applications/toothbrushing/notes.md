

# TODO

PoC with ML

- Test on device
- Record more data. Get up to 8 or 10 sessions total.
- Move project to its own repository. Under jonnor?
- Record a demo video
Maybe plot the state/counters as overlay?

Misc

- Setup quantitative evaluation of time tracking.
Cut out random selections of time-sections.
- Design a basic dock. With magnetic connector
https://www.kjell.com/no/produkter/kabler-og-kontakter/usb-kabler/plexgear-magnetisk-usb-c-adapter-p44923
- Add battery voltage/power/percent tracking

Later

- Send prediction data over BLE. To phone
- Send sensor data over BLE. For data collection
- Enable sleeping, test battery life

# Installing



# Sound design

https://onlinesequencer.net

Online Sequencer:923227:0 C5 1 43;2 D#5 1 43;1 D5 1 43;4 F5 1 43;5 F#5 1 43;6 G5 1 43;8 A5 1 43;9 B5 1 43;10 C6 1 43;12 D6 1 43;13 D#6 1 43;14 F6 1 43;17 C6 1 43;18 G5 1 43;19 E5 1 43;21 C5 4 43;:

# Data

### Custom dataset

Data collection protocol.

Using har_record.py from har_trees emlearn-micropython example.

Configure the RTC.

Brushing.

Session should be 3 minutes long.
Start with toothbrush standing.
Brush like normal.
Take a number of pauses of 5-10 seconds duration. Around 5-10 pauses per session.

- Swap toothbrush between hands.
- Hold toothbrush completely still in mouth
- Take toothbrush out of mouth to talk
- Put toothbrush down on surface, pick up again
- Swing arms down
- Walk around with toothbrush in hand
- Stretch with arms overhead
- Drop the toothbrush in the sink
- Rinse the toothbrush
- Put more toothpaste on toothbrush
- Other (subject decides)
- Check something on the face in the mirror
- Talk to someone
- Drink water from tap
- Turn tap off/on
- Inspect/poke at teeth


Other

- Walking around indoor, toothbrush in hand
- Walking in stairs, toothbrush in hand
- Playing swords with toothbrush
- Sitting down/up, toothbrush in hand
- Dropping toothbrush onto surface
- Throwing toothbrush onto surface
- Toothbrush lying on surface
- Throwing toothbrush into the air, flipping
- Tapping on toothbrush
- Inspecting toothbrush
- Walking with toothbrush in backpack
- Driving with X in backpack
- Biking with X in backpack

Ideally record video. Using phone.
Time syncronization.
Tap the brush 5 times to surface at start and end.

N sessions. Want something like 10+.
N subjects. 
Between sessions.

Labeling precision target.
Better than 1 second. Not needed as good as 100 ms.

First target. 5 sessions, 1 subject.

ffmpeg -i input.avi -c:a copy -vf "scale=-2:720" -c:v libx264 -pix_fmt yuv420p -crf 23 output.mkv

ffmpeg -ss 00:03:00 -i input.mkv -c copy output.mp4

Download links in Google Drive

https://drive.google.com/uc?export=download&id=FILEID


#### Dataset for toothbrushing activity using brush-attached and wearable sensors
https://www.sciencedirect.com/science/article/pii/S2352340921005321
https://data.mendeley.com/datasets/hx5kkkbr3j/1
https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/hx5kkkbr3j-1.zip

Toothbrushing data for 120 sessions performed by 22 participants (11 males, 11 females).
The data was collected using two IMU devices from Mbientlab Inc.
One device was attached to the brush handle, while the other device was used as wearable (wristwatch on the brushing hand).
The participants brush their teeth for around two minutes in each session following a pre-given sequence.

235 MB total.

## Hardware

- Needs accelerometer/IMU.
- And some way of notifying user. LED and/or buzzer.

For prototyping the M5StickC can be used.
A bit bulky, but workable.

Then the `dml20m` hardware would be used to actually demonstrate the 1 USD TinyML concept.

## References

#### Development and evaluation of the “Toothbrushing Timer with Information on Toothbrushes” application: A prospective cohort pilot study
https://pmc.ncbi.nlm.nih.gov/articles/PMC10728532/

A mobile phone app to help users ensure appropriate toothbrushing time and learn about the beneficial characteristics of toothbrushes

#### Separating Movement and Gravity Components in an Acceleration Signal and Implications for the Assessment of Human Daily Physical Activity

We aimed to evaluate five different methods (metrics) of processing
acceleration signals on their ability to remove the gravitational component of acceleration during standardised mechanical
movements and the implications for human daily physical activity assessment.

Euclidian norm minus one (ENMO),
Euclidian norm of the high-pass filtered signals (HFEN),
HFEN plus Euclidean norm of low-pass filtered signals minus 1 g (HFEN+)


#### Gravity subtraction

Should establish the initial gravity vector for calibration.
When standing in holder.

To leave out the gravity vector from the accelerometer value, you need to rotate the accelerometer vector to the earth frame using a rotation matrix or quaternion which can be calculated from accelerometer, gyroscope, and magnetometer.
After you rotate the vector to the earth frame you can subtract the (0, 0, g)^T vector to take out the gravity.
You can rotate the resulted vector to the body frame again by multiplying the inverse matrix of the rotation matrix that you have used before

https://math.stackexchange.com/a/1746199/1519080 
Python/numpy code

https://howtomechatronics.com/tutorials/arduino/how-to-track-orientation-with-arduino-and-adxl345-accelerometer/
https://www.allaboutcircuits.com/technical-articles/how-to-interpret-IMU-sensor-data-dead-reckoning-rotation-matrix-creation/

Freescale AN3461: Tilt Sensing Using a Three-Axis Accelerometer

https://josejuansanchez.org/android-sensors-overview/gravity_and_linear_acceleration/README.html
Simple java code using 

## Existing products

There are timers.
Especially targetting kids.
Some are using an hourglass principle using colored oil.

Some are electronic using light to indicate done.

Braun has "Genius X" series.
https://www.oralb.co.uk/en-gb/product-collections/genius-x
An electric toothbrush with "Artificial Intelligence".
Tracks where you brush in your mouth.



## Asides

#### Adverserial usage

If someone is trying to fool the device that they are actually brushing their teeth,
can we actually separate that from actual toothbrushing?
Like vigorous shaking. At approximately the right periodicity.
At approximately the right angle even?
Probably not...
But including some roughly similar data from other semi-energetic activities might be a good check for robustness.

