
# Air Quality

With Air Quality sensors one wants to estimate values for potential pollutants,
such as PM2.5, NO2, CO, CO2, SO2, O3.
Low-cost sensors are subject to cross-sensitivities, and environmental factors.
Correcting for this is usually called "calibration".

This.
Common methods are

- Multiple Linear Regression
- Random Forest Regression
- Support Vector Machine Regression
- Multi layer Perceptron neural network

The gas sensors used are often of Metal Oxide semiconductor (MOX) type.

## Datasets

### UCI Air Quality Data Set
https://archive.ics.uci.edu/ml/datasets/Air+quality
Released in 2016

Array of 5 metal oxide chemical sensors embedded in an Air Quality Chemical Multisensor Device.
9358 instances of hourly averaged responses.
The device was located on the field in a significantly polluted area, at road level, within an Italian city.
Data were recorded from March 2004 to February 2005 (one year).
Ground Truth hourly averaged concentrations for CO, Non Metanic Hydrocarbons, Benzene, Total Nitrogen Oxides (NOx) and Nitrogen Dioxide (NO2),
were provided by a co-located reference certified analyzer. 

### Air Quality dataset for ADL classification
Activities of Daily Life
https://data.mendeley.com/datasets/kn3x9rz3kd

Array of 6 low cost sensors. One sensor value (concentration) from each.
Classes
1 - Normal situation - Activity: clean air, a person sleeping or studying or resting - Samples: 595;
2 - Preparing meals - Activities: cooking meat or pasta, fried vegetables. One or two people in the room, forced air circulation - Samples: 515.
3 - Presence of smoke - Activity: burning paper and wood for a short period of time in a room with closed windows and doors - Example: 195.
4 - Cleaning - Activity: use of spray and liquid detergents with ammonia and / or alcohol. Forced air circulation can be activated or deactivated - Samples: 540. 

### UCI Gas sensors for home activity monitoring Data Set
http://archive.ics.uci.edu/ml/datasets/Gas+sensors+for+home+activity+monitoring

Gas sensor array composed of 8 MOX gas sensors, and a temperature and humidity sensor.
This sensor array was exposed to background home activity while subject to two different stimuli: wine and banana.
The duration of each stimulation varied from 7min to 2h, with an average duration of 42min.

### UCI Gas Sensor Array Drift Dataset Data Set
https://archive.ics.uci.edu/ml/datasets/Gas+Sensor+Array+Drift+Dataset
Published 2012

13910 measurements from 16 chemical sensors utilized in simulations for drift compensation in a discrimination task of 6 gases at various levels of concentrations.
Six distinct pure gaseous substances, namely Ammonia, Acetaldehyde, Acetone, Ethylene, Ethanol, and Toluene, each dosed at a wide variety of concentration values ranging from 5 to 1000 ppmv.

### Dataset for "Characterization of inexpensive MOx sensor performance for trace methane detection"
https://experts.umn.edu/en/datasets/dataset-for-characterization-of-inexpensive-mox-sensor-performanc
Published 2022

Laboratory calibration data for three replicates each of five types of inexpensive methane sensors in support of a study characterizing sensor suitability for atmospheric monitoring, with particular attention to sensitivity to humidity and temperature. Sensor performance from ambient levels to 10ppm was characterized with decaying methane pulses at five different temperatures.

### H2020 project CAPTOR: raw data collected by low-cost MOX ozone sensors in a real air pollution monitoring network
Published 2021

https://www.data-in-brief.com/article/S2352-3409(21)00411-X/fulltext
https://zenodo.org/record/4570449

25 nodes in Spain.
Each node had four SGX Sensortech MICS 2614 metal-oxide, for redundancy.

## Papers

### What Influences Low-cost Sensor Data Calibration? - A Systematic Assessment of Algorithms, Duration, and Predictor Selection
https://aaqr.org/articles/aaqr-22-02-oa-0076
June 2022


### Calibration of a low-cost PM2.5 monitor using a random forest model
https://www.sciencedirect.com/science/article/pii/S0160412019322780
December 2019

random forest model showed better performance than the traditional linear regression model
Features: temperature, relative humidity
! only tested in lab
!! only a single test run, on a single device

https://ui.adsabs.harvard.edu/abs/2018AMT....11..291Z/abstract


### A machine learning calibration model using random forests to improve sensor performance for lower-cost air quality monitoring 

https://ui.adsabs.harvard.edu/abs/2018AMT....11..291Z/abstract
January 2018

Real-time Affordable Multi-Pollutant (RAMP) sensor package, which measures CO, NO2, O3, and CO2
Training and testing windows spanning August 2016 through February 2017 in Pittsburgh, PA, US.
The random forest models matched (CO) or significantly outperformed (NO2, CO2, O3) the other calibration models,
and their accuracy and precision were robust over time for testing windows of up to 16 weeks.
Following calibration, average mean absolute error on the testing data set from the random forest models was
38 ppb for CO (14 % relative error),
10 ppm for CO2 (2 % relative error),
3.5 ppb for NO2 (29 % relative error),
3.4 ppb for O3 (15 % relative error)
Pearson r versus the reference monitors exceeded 0.8 for most units

### Non-linear Machine Learning with Active Sampling for MOX Drift Compensation

Evaluated on UCI’s HT detectors. Banana/wine/background


## Electronic nose
https://ieee-dataport.org/keywords/electronic-nose


https://ieee-dataport.org/documents/mixed-explosives-dataset
https://ieee-dataport.org/documents/dataset-electronic-nose-various-beef-cuts
https://ieee-dataport.org/documents/dataset-pork-adulteration-electronic-nose-system


