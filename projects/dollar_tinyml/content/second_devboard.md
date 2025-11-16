
## Rev2 Motion devboard arrived

Back in January I finished the rev 2 board (mentioned in previous post).
PCBWay proposed to sponsor the board, and it was finished and arrived in just a few weeks time.
The board is very well made, as I have come to expect from them (I use them also for work).


I have confirmed that I can program the microcontroller and done some basic checks of the LEDs, etc.
Unfortunately this year has been very busy, so I have been unable to do more checks of the board.

However, I was able to improve the software stack for doing motion classification with emlearn.
There is now a C implementation of a motion preprocessor / feature extractor, in addition to the MicroPython preprocessing code that already existed.

https://github.com/emlearn/emlearn/tree/master/examples/motion_recognition
https://github.com/emlearn/emlearn-micropython/tree/master/examples/har_trees

Last Christmas I also created another example project,
an automatic toothbrush timer that uses the accelerometer to classify time being actively spent brushing.
It is currently running MicroPython with emlearn-micropython on an ESP32-based device from M5Stack.
I am now porting this to this board, using the above C preprocessing code.

https://github.com/jonnor/toothbrush/
https://youtube.com/shorts/TgG-jxXNJIs?si=bGGplUQlYsZlruNr

IMAGE. Features over time? Gravity decomposition

Trying out the board for the toothbrush usecase revealed a few shortcomings.
The main one being that it would be nice to have a USB Type-C socket instead of Type A edge connector,
to avoid something sticking out of the device. Such connectors are now

IMAGE. Board and toothbrush.

For now I have done a quick hack by soldering on an external USB Type-C connector breakout.
But this is something I am considering changing for future revisions.



