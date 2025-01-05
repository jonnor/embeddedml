
## PIR

PIR element around 25 cents.
PIR controller IC around 5 cents. Ex: EG4002

https://www.lcsc.com/products/Human-Body-Sensing-Sensor_11283.html



## LED based spectroscopy

A Simple Spectrometer Using Various LEDs and a Photodiode Sensor for Photocatalytic Performance Evaluation
https://www.researchgate.net/publication/276412262_A_Simple_Spectrometer_Using_Various_LEDs_and_a_Photodiode_Sensor_for_Photocatalytic_Performance_Evaluation

Measure waste water clarity after the photocatalytic treatment.
Simple spectrometer consisting of LEDs with different colors (white, red, blue, green and yellow) as light sources,
a cuvette as vessel of the sample, and a photodiode OPT101 as sensing element.
The red LEDs gave an average error of less than 5%, which is comparable to that obtained by the commercial UV-Vis. 


A promising approach to creating cost-effective spectrometric devices is using a LED & Photodiode Based Spectrometry,
where a set of LEDs tailored to the desired wavelength region and one or more photodiodes (PDs) are used for detection. 
https://www.joyateam.com/post/led-photodiode-based-spectrometry


The AS7265x family incorporates 3 chips to deliver an 18-channel multi-spectral sensing array covering wavelengths from 410nm to 940nm.
https://learn.sparkfun.com/tutorials/spectral-triad-as7265x-hookup-guide/all
shows the wavelengths.

Closest common LED. Per DigiKey

410  405
435  rare!
460  460/465
485  470
510  503
535  530
560  rare!
585  590
610  600/620. Rare
645  630/650
680  660
705  rare!
730  720-740. Bit rare
760  770. Bit rare
810  810/830. Bit rare
860  860
900  890
940  940

7-8 channels might be doable with regular LEDS.


https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3836
has 14 LEDs, from 365 nm to 660 nm

Simtrum Wavelength-Switchable LED Source (340-980nm)
https://www.simtrum.com/WebShop/ProductList5.aspx?pid=1770
Offers up to 9 LED emitters, that can be rotated.
From a selection of 26 narrow band, and 4 broad band LED sources.

```
WLS-LED-0340-02	340	3.4	500	4.3	23
WLS-LED-0365-04	365	3.4	1000	3.65	350
WLS-LED-0385-04	385	3.4	1000	3.65	500
WLS-LED-0400-01	400	2.5	350	3.5	100
WLS-LED-0405-03	405	1.7	1000	3	325
WLS-LED-0410-03	410	1.7	1000	3	315
WLS-LED-0415-03	415	1.7	1000	3	310
WLS-LED-0420-03	420	1.7	1000	3	310
WLS-LED-0425-03	425	1.7	1000	3	290
WLS-LED-0455-03	455	1.7	1000	3.9	280
WLS-LED-0470-03	470	1.7	1000	3.9	200
WLS-LED-0490-01	490	1.7	350	3.5	140
WLS-LED-0505-03	505	1.7	1000	3.9	135
WLS-LED-0530-03	530	1.7	1000	3.9	100
WLS-LED-0560-02	560 broadband	1.7	700	2.9	180
WLS-LED-0590-03	590	1.7	1000	3.9	65
WLS-LED-0617-03	617	1.7	1000	3.9	150
WLS-LED-0625-03	625	1.7	1000	3.9	280
WLS-LED-0656-03	656	1.7	1000	2.7	280
WLS-LED-0680-02	680	1.7	600	2.7	75
WLS-LED-0740-03	740	2.5	1000	2.5	200
WLS-LED-0780-02	780	1.7	800	2.5	110
WLS-LED-0810-02	810	1.7	800	2.2	120
WLS-LED-0850-02	850	1.7	1000	2.1	175
WLS-LED-0870-01	870	1.7	700	1.9	110
WLS-LED-0940-01	940	1.7	700	1.5	100
WLS-LED-0940-02	940	1.7	1000	1.8	200
WLS-LED-0980-01	980	1.7	500	1.4	30
WLS-LED-4000-03	warm white 4,000K	1.7	1000	3.9	180
WLS-LED-5500-03	cool white 5,500K	1.7	1000	3.9	170
WLS-LED-6500-03	glacier white 6,500K	1.7	1000	3.6	180
```

Uses discrete LEDs as the source, on a stepper-driven color wheel.
Uses AS7341 10-channel color sensor as the sensor.
https://hackaday.com/2024/12/28/a-low-cost-spectrometer-uses-discrete-leds-and-math/#comment-8077456

