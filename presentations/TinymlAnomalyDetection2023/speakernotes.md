
## WPM
100-150 words per minute
10 minutes, 1000 words max

## Disposition

#### Hello

Hi everyone.
Presenting a case studies revealing success in Predictive Maintenance and Anomaly Detection.
We will include our learnings from the last 3 years of testing out this usecase in the market.

#### Commercial buildings
Just to make sure we are on the same page.

Commercial buildings are buildings used primarily for commercial purposes,
includes includes office, hotels, restaurants, shops etc.
But many times the term also includes schools etc.
Basically anything that is not residential or industrial.

--- 1 minute

#### Expectations in a commercial building
A commercial building is used by its tenants and guests.
As users in a building, they have the expectation that the building functions well.
This includes a wide range of services, which may depend on the building.
But practically every building must provide clean air, heating and cooling.

Behind the scenes this requires various machinery,
and there is a buildings operations team responsible for keeping it functional.

Often the term Heating, Ventilation and Air Conditioning (HVAC) is used for this.
And it is a constant job to maintain the system,
as it is subject to mechanical and electronic breakdown.


#### Todays maintenance of HVAC
Most commercial buildings rely mostly on manual inspections

A typical schedule for check-ins would be:

    Every 1-2 weeks by building operations team
    + Every 6-12 months by service technicians

In most cases, there is nothing to report.
Would be better to spend the time on more impactful activities.
And even with a strict adherence, issues slip by and cause downtime.

--- 2 minute

#### Remote condition monitoring

With Condition Monitoring one continiously measure the health of machinery.

Benefits of Condition Monitoring
    Improved ability to plan activities
    More efficient use of time
    Reduction in unplanned downtime
    Faster recovery from downtime

Benefits of Remote monitoring 

    Less time spent on transportation to check machine condition
    Monitor equipment in larger geographic area, Economy of scale



### Air Handling Units

All buildings need ventilation
Air Handling Unit is the central machine for this function

Valuable place for Condition Monitoring, because

High impact on tenant when not functional - bad air quality
High energy costs in case of incorrect operation

-- 3 minutes

### Vibration Monitoring for Air Handling Unit

Installed vibration sensors on the rotating components of Air Handling Unit.
Supply Fan, Exhaust Fan, and motor for Rotating Heat Exchanger
This covers the major mechanical components of the system.

Vibration sensors are low-cost units with a MEMS accelerometer.
Battery powered for ease of install.
Transmits vibration data every 1 minute.
To an IoT gateway, that sends data to a cloud service, using 4G cellular or Ethernet.

### Sensor data quality
Industrial vibration sensors costs often costs in excess of 1000 USD.
This is too high for commercial buildings.

Does the MEMS accelerometers have sufficient performance?

To evaluate this we did a series of controlled tests.
Both in lab environment where we could do destructive tests,
and in field where we did stress testing within safe limits.

Was able to verify that MEMS accelerometer sensors can detect
a range of problematic conditions.
Such as shaft misalignment, bearing failure, unusually high load, etc

-- 4 minutes

### Normal conditions

We realized quickly that the vibration data from different equipment varied widely.

Based on the equipment type/brand/model, sensors placement, and component condition.

Also the way that the equipment is being operated differed considerably.

For ventilation systems it is very common to have timer-based schedules
based on when the building is in use.

To handle this complexity in the "normal" data we use Machine Learning
to automatically learn the patterns of a particular device.

### Anomaly Detection

For the Anomaly Detection approach we have tested a range of different models.

We are mostly looking for anomalies over longer periods of time
that are indicative of a change in machine condition or state.
1 hour or more, from 1 minute sensor data.
Such sequences of anomalous datapoints is known as collective anomaly.

Currently we are using custom developed models based on the CAPA model,
which is especially designed to handle collective anomalies.

-- 5 minutes


### Example 1

We are currently monitoring over 1000 components in many buildings in Scandinavia.

Here is a motor for the heat exchanger that started to get erratic vibration.
An alarm was raised, and operations team confirmed it was about to stop functioning.
Were able to get a replacement done before functionality stopped.

!! issue appeared just 1 week after service technician had done a bi-yearly service

### Example 2

Vibration level started increasing after having been flat for many months.
Extra clear when compared to the supply fan (which is under same operation conditions),
which stayed nice and flat.

Service technician confirmed that bearing was failing and scheduled a replacement.

### Example 3

One somewhat suprising learning was that it is quite common in buildings
that equipment are ON when they should be OFF,
or OFF when they should be ON.
 
There are a wide range of sources for this, including
configuration problems, software bugs, communication problems.

Here is an example of a system that was running day and night.
This was spotted during the installation.
However the system will also automatically raise alarm if this starts occuring.

This is not really predictive.
But according to customers the typical detection time for these problems can be weeks,
so in practice one gets a much better time-to-resolution.


### TinyML opportunity

The system described previously uses a classic DSP system to extract vibration.
This is already very useful, as the examples show.

However it is know from Condition Monitoring literature
more advanced machine health analysis for vibration data,
which can give an even better machine health estimation.

For example rotation speed, starts/stops, changes in frequency spectrum etc.

We believe TinyML will be a key,
and are starting to test such systems now.


### Summary

Benefits from Condition Monitoring transfer well to HVAC

Gains are comparatively smaller - CM system must be low-cost

Vibration monitoring with wireless MEMS sensors can effectively detect many problems

Air Handling Units are a valuable target for CM in commercial buildings

Anomaly Detection is a key technique for automated detection

Potential for even better detection via on-sensor Machine Learning

