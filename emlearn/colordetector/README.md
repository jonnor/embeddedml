
# TODO

First PoC

- Train a classification model for cards
- Deploy model to device, test it
- Add logging of predictions

Object detector demo

- Print and use 3-led version
- Get some fun colored object
- Collect data and train model
- Make a demo video

## Later

- Design a PCB and send to manufacturing
Support both throughhole components and SMD
5mm LEDs / SMD LEDs (1206 ?)
Using Arduino shield form factor?
Maybe have pieces that can be cutout to act as distace meters

# Instructions
 
## Electronics assembly

`TODO: add schematics`
`TODO: add breadboard drawing / Fritzing`

## Flashing firmware

`FIXME: write instructions`

## Labeling data

Find a set of objects representing the classes to detect.

Write down the name, class and colors of objects into a `objects.csv` file.

`FIXME: support loading this CSV file into training pipeline`

Run the colordetector code on device.

Start the data collector.

```
python colordetector.tools.logdata --out data/myobjects-1.csv
```

`FIXME: logdata should refuse to overwrite existing data`

Present each object in turn, following the order you have defined.
When the object is fully above the sensor, press and the hold button for 5 seconds.
Do not move object until button is released.

Do this for each object.

Recommend repeating the entire sequence of objects 3 times.


## Training model

`FIXME: make and test training script`

```
python colordetector.train --data-files data/myobjects*.csv --out build/model-1/ 
```

## Deploy model onto device

`FIXME: write instructions`

