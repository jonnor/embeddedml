
## Title
HVAC monitoring in commercial buildings using anomaly detection

## Abstract

There are millions of commercial buildings in the world, from offices, to schools, hospitals and stores.
Most of these are fitted with heating, ventilation and air conditioning (HVAC) systems,
in order to provide a productive and comfortable indoor climate.
As with all electromechanical systems, HVAC systems are subject to breakdowns
and must be maintained in order to keep them functional.
The most common strategy is time-based inspections by the building operations personnel and HVAC service providers.
This labor-intensive approach is costly, but many failures still slip by because they happen between inspection intervals.

In early 2022, Soundsensing started to deploy condition monitoring to HVAC systems in commercial buildings.
The solution uses vibration- and sound-sensors to monitor rotating equipment in these systems.
We find that the system is able to provide early-warning for many mechanical issues,
enabling operations teams to schedule maintenance before the system goes down.
Furthermore, we find that many systems repeatedly have problems with running when they should not,
or not running when they should - and that most of the buildings lack Building Management Systems
that accurately detect these issues.
Both of these failure modes are monitored using an Anomaly Detection approach,
and combined, the system provides both cost savings and lower downtime.

## Section
Case studies revealing success in PdM and AD

## Format

10 min for your presentation

5-10 slides

We look for technical value, use case and no corporate marketing please.

## Story arcs

Alt A. Discovery. Learning journey. First this, then that.
! 10 minutes maybe too short
Can be too rambly. More suited for more personal venues/formats

Alt B. Thesis investigation and results.
Key questions. And answers

Alt C. Parallel to know (hi)story
CM was introduced in heavy asset industry in
Compare & contrast

Primariry alt B, with minor aspects of Alt C

## Take aways

Condition Monitoring is valuable for HVAC systems
    +   mechanical 

Vibration monitoring is established best practice for rotating machinery from industry

MEMS 

Soundsensing has a mature solution
    + Already used by many buildings



## Challenges

Plug & Play.
No integration with building management system required.
No or very little per-machine / per-site configuration

Costs must be low to be cost-efficient
In traditional CM applications


Differences in levels. Based on
- equipment type and model
- existing equipment condition (which is unknown)
- placement and attachment method (which has to be practical). Motors rarely designed

Timer schedules

Demand-driven ventilation


Next steps: Improved support for demand-driven ventilation
Image: Curves of rotation speed / current versus


## Key questions

How can CM sensors with automated analysis benefit commercial buildings?
    Same way as in traditional industry
    Known benefits
    Though the direct savings from reduced downtime is lower

What are the most valuable use-cases?
    Air Conditioning

Does cost-effective hardware exist?
Can off-the-shelf hardware be used?

    MEMS vibration monitors. Battery powered, Bluetooth LE

What kind of user experience should it have?

    Very few false positives
    Only want alarms for the most severe issue
    Few days - few week heads up is good. No need to detect months in advance. 

How to enable plug & play system
    Learned configuration
    Anomaly Detection paradigm

What is the cost/benefit for CM in commercial buildings?
    Not discussed here, mostly focusing on tech


## Learnings

Many buildings do not have Building Management System
    some do not have remote access
Many Building Management Systems do not have proper feedback
    - control systems assume success
    - missing/incorrect configuration of alarms

Even the most recent BMS do not have anything for mechanical failures

Manual inspections the main strategy
    By operations team. Possibly weekly. 
        ! tends to get down-prioritized at busy times

Vibration monitoring not widely deployed

High percentage of buildings have timer/schedule based HVAC
Last converted from fixed function during 2022 - due to unusually high energy prices in Norway
Have already been the norm many other countries for several years

Control issues is a real problem in many buildings

Frost-guards can prevent HVAC system from starting up
Typically needs manual reset
Without an online BMS cannot tell when

Retrofitting an online BMS to a building is very expensive


Teams often manage multiple buildings
Buildings have different equipments
Want a unified solution

Have existing work order systems.
Professional organizations are on a track to use these for all work
Integration of CM systems highly desirable

Run to failure is standard
Low cost of failure - compared to industry

Building operators are not interested in configuring or setting up tech themselves,
or to pay for very costly integrations.
They want to buy fully-operational technology

MEMS accelerometers give sufficient quality

Bluetooth Low Energy works in technical room setting
    Metal cabinets
    Range with 4.2 some 10s of meters
    Still requires some care regarding gateway positioning

Most buildings do not have Ethernet connecticity
Not particularly interested in adding either
4G working well for 95% of cases.
Even in basements!
Remaining requires extra care with antennas
Ethernet can be used as a fallback


## Goals

Reduce manual 
Catch errors before failure

## Timeline

Q2 2020 - student project
Q4 2021 - PoC testing
Commercial lauch
Q3 2023 - 
    NN buildings

Q3 2023. >1000 components

## Images

Pictures of sensors deployed in the field
Pictures of data from live dashboard
A couple of usecases shown

Photo collage of installed sensors

## Tech

Use a variation of CAPA

Collective And Point Anomalies (CAPA)


## Audience

Pdm/AD forum.
Assuming that they know about Predictive 

## Known from industry

Vibration monitoring one of the useful tools for rotating machinery



## Call to Action

Expanding to Europe in 2024 onwards.



