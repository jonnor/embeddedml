
# TODO

First Object detector demo

- Make the dataset configurable. Unhardcode colors
- Plot colors in sequence for dataset
- Add 3 LEDs to indicate the class
- Test without a holder. Just the LEDs sticking up
- Test using ambient light as source, instead of white LED
- Clean up notebooks. Move longer functions to .py files
- Get some fruits to test with
- emlearn: Add class name generation. Enum+strings
- Make a demo video
- Finish the documentation below

Improve docs

- Move into an emlearn-demos repository
- Setup a Sphinx build
- Publish to read-the-docs

Better model

- Implement color space transformations and 2d reduction
- Implement centroid classifier in emlearn? With distance support

Handling unseen data

- Make examples of handling unseen data
- Write user guide on handling unseen data 
- Make a demo that shows unseen objects



## Later

- Switch to 4-led (RGBW) version of the holder

### Custom PCB
- Design a PCB and send to manufacturing
Support both throughhole components and SMD
5mm LEDs / SMD LEDs (1206 ?)
Using Arduino shield form factor? Or just DIP for easy breadboarding
Maybe have pieces that can be cutout to act as distace meters

## On-device learning

- Implement kNN or similar in emlearn
- Create a new demo for it

# Instructions
 
## Electronics assembly

`TODO: add schematics`
`TODO: add breadboard drawing / Fritzing`

## Flashing firmware

`FIXME: write instructions`

## Collecting data

Find a set of objects representing the classes to detect.

Write down the name, class and colors of objects into a `objects.csv` file.

`FIXME: support loading this CSV file into training pipeline`

Run the colordetector code on device.

Start the data collector.

```
python colordetector.tools.logdata --out raw_data/myobjects-1.csv
```

`FIXME: logdata should refuse to overwrite existing data`

Present each object in turn, following the order you have defined.
When the object is fully above the sensor, press and the hold button for 5 seconds.
Do not move object until button is released.

Do this for each object.

Recommend repeating the entire sequence of objects 3 times.

For 10 objects it should take around 5-10 minutes in total.

## Making curated dataset

The data collector above just logs the raw events sent over serial.
We will transform this into a structured dataset for model training.

This uses the information provided about ordering to label the data.

```
python colordetector.preprocess --data-order myobjects.csv --data-files raw_data/myobjects*.csv --out dataset/myobjects/
```

`FIXME: output plots of the data to output folder`
`TODO: describe how to check the data`

## Training model

`FIXME: make and test training script`

```
python colordetector.train --data-files data/myobjects*.csv --out build/model-1/ 
```

## Deploy model onto device

`FIXME: write instructions`



