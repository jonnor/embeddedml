
# Gesture recognition

## Demo idea: magic wand

Use the magic wand project as a base. With Arduino Nano33 BLE Sense.
Replicating the on-host training and on-device inference would be nice.
See if can match performance and maybe reduce computational complexity.

But the killer demo would be to support on device training.
To allow on-the-fly custom gestures.

Would also be nice to add battery and a proper wand look.
Just 3d-print / hack something.

Video should turn something on/off using the BLE data. For example using a bridge to like Home Assistant, and then to some ESP32 device, et.c
Or it could be a BLE controlled device. Like another  Nano33 - easier to replicate.
Or a BlueFruit, same microcontroller but also has Neopixels on board 
https://www.adafruit.com/product/4333

## Related

Gesture recognition with capacitive sensing.
Using multiple capacitive sensors.
Supported on many microcontrollers.


## Existing works

#### jewang/gesture-demo

https://github.com/jewang/gesture-demo

The wand detects gestures as inspired by the Harry Potter and the Sorcerer's Stone computer game.

- W (wingardium leviosa)
- spiral (flippendo) 

Key aspects

- Using Raspberry PI Zero
- Training in Python on PC / computer
- Using scikit learn on hand computed features


### petewarden/magic_wand
https://github.com/petewarden/magic_wand

Demo for Tensorflow Lite micro.
Uses Arduino Nano33 BLE Sense.
Mounted to end of a stick. Standard orientation
Has web interface for collecting data

Has 4 classes, 3 gestures pre defined

- Ring O
- Wing W
- Slope l/v
- Random, anything else

https://colab.research.google.com/github/petewarden/magic_wand/blob/main/train/train_magic_wand_model.ipynb
Model does a projection onto X,Y plane,
and then uses an image/CV style CNN
Not time-series!

Nice visual representation.
Intuitive.
We are "painting" with the wand.

### Neutron: Making famous magic wind 33x faster

https://neuton.ai/news/projects/84-making-famous-magic-wand-33x-faster.html
Claims to reduce inference time from 55ms to 1.5ms
Says sensor uses XYZ accelerometer values at 100hz, with a 2 second window

Collected their own data
https://github.com/Neuton-tinyML/magic-wand-data-that-we-have-collected
Possibly different protocol 


