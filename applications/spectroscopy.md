
## UV-Vis spectroscopy



## Principle of operation

Absorbance.

Transmittance is the ratio of the source radiation’s power as it exits the sample, PT,
to that incident on the sample, P0. `T=PT/P0`.
Multiplying the transmittance by 100 gives the percent transmittance, %T,
which varies between 100% (no absorption) and 0% (complete absorption). 

Absorbance, A, defined as `A = −log(T) = −log(PT/P0)`.


Beer–Lambert (BBL) law.
https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law
Beer–Bouguer–Lambert (BBL) extinction law is an empirical relationship
describing the attenuation in intensity of a radiation beam passing through a macroscopically homogenous medium with which it interacts.

UV-vis spectrocopy. Typically from 190nm to 900 nm.
A more narrow range of for example 300 nm to 700 nm may be used.
From around 400 nm is visible light.

VIS-NIR spectrometers might have a range of 500 - 1100 nm.

IR spectrocopy uses longer, lower-energy wavelength range.
Typically 4,000 to 400 cm-1 (2,500 to 25,000 nm),
but this can extend to 7,000 to 350 cm-1 (1,400 to 28,000 nm).

Building a Nanodrop Style UV/Vis Spectrometer (2016)
https://www.youtube.com/watch?v=pIk8I10ZmYY
Explains absorbance and usage for determining fluid concentration,
and how fluoresence can be used to quantify DNA.

## Refences

Theremino project has a lot of info.

"Diffraction Grating Spectrometer, Design and Collected Spectra, Theremino System" has 85 pages of good stuff.
Includig spectra from interesting compounds. Including Hemoglobin, 
UV flourestnce spectroscopy. Using 405 nm exitation, mostly.

> In the spectrum of “Extra Vergine” olive oil, obtained by cold pressing you notice the absence of the
products of peroxidation of fatty acids, which give fluorescence at about 470nm. This happens both
because the oil is cold worked and because the high content of natural anti-oxidants (carotenes and
polyphenols ) prevents oil from oxidative degradation.

Shows different oils. Peanut, olive, sunflower, corn, soybean, almond, sesame, castor.
Shows also thermally degraded oils.


## Project 1, oil quality

Edible oil. Quality estimation. Poor storage. Oxidation.

- Refined olive oil vs extra virgin
- Old extra virgin vs new
- Olive oil adulterated with sunflower/rapeseed

Price of olive oil vs others.
https://www.indexmundi.com/commodities/?commodity=olive-oil&months=120&commodity=palm-oil
Can download edible oil prices.
Excel possible with free account


### Related work

EVOO, BO, and SO
https://www.edinst.com/resource/application-note-olive-oil-quality-assessment-with-uv-vis-spectrophotometry/
Shows different concentrations.
Big differences at 330-420nm.


#### Application of steady-state and time-resolved fluorescence spectroscopy in identification of cold-pressed vegetal oils

Fluorescence emission spectra of the studied cold-pressed vegetal oils:
walnut oil – OW, corn oil – K, roasted peanut oil – A, Extra Virgin Olive oil – O, sunflower oil – S.
Excitation wavelength: (a i b) λexc=290 nm, (c) λexc=320 nm, (d) λexc=350 nm, (e) λexc=405 nm

The most evident differences in the shape of the fluorescence bands
were obtained in the emission spectrum at
λexc = 350 nm and in the excitation spectrum at λem = 500 nm

#### Validation of Fluorescence Spectroscopy to Detect Adulteration of Edible Oil in Extra Virgin Olive Oil (EVOO) by Applying Chemometrics

https://journals.sagepub.com/doi/abs/10.1177/0003702818768485?utm_source=chatgpt.com

In this study, adulteration of edible oil (sunflower oil) is made with pure EVOO
and analyzed using fluorescence spectroscopy (excitation wavelength at 350 nm).

365 nm quite commmon and affordable. 


#### Quantitative Detection of Extra Virgin Olive Oil Adulteration, as Opposed to Peanut and Soybean Oil, Employing LED-Induced Fluorescence Spectroscopy 
https://www.mdpi.com/1424-8220/22/3/1227?utm_source=chatgpt.com

Eight LEDs with central wavelengths from ultra-violet (UV) to blue are tested to induce the fluorescence spectra of EVOO, peanut oil, and soybean oil, and the UV LED of 372 nm is selected for further detection.
Samples are prepared by mixing olive oil with different volume fractions of peanut or soybean oil, and their fluorescence spectra are collected.

! used reflectance. Emitter 45 degree from top, 

Eight LEDs with a central wavelength of
370 nm, 372 nm, 396 nm, 402 nm, 414 nm, 441 nm, 451 nm, and 465 nm
were employed to excite the fluorescence
of pure EVOO, PO, and SO samples, respectively.
An acquisition time of 1 s was used. 

However, the light sources used in [17,18] were lasers,
which are narrow in bandwidths (typically less than 1 nm) compared to that of LEDs (typically ten to twenty nanometers).
Another phenomenon that can be observed is that the longer the central wavelength, the wider the bandwidth.

Thus, though lasers of wavelength larger than 440 nm can be utilized for oil adulteration detection, LEDs of this band are not suitable, because their own spectrum may overlap with the fluorescence spectrum. Thus, the excitation wavelength of 372 nm was selected.


#### Monitoring of oxidative stability of olive oils using visible spectroscopy
https://www.researchgate.net/publication/344100936_Monitoring_of_oxidative_stability_of_olive_oils_using_visible_spectroscopy
Measured 350-700nm.

The spectral changes during oxidation were analysed using principal component analysis (PCA). Partial least squares (PLS) regression analysis was used to quantify the relationship between chemical parameters, peroxide and acid values, and oil spectra. It was found that visible spectroscopy can be used to evaluate the oxidative changesof olive oils.


#### Pigments in Extra‐Virgin Olive Oil: Authenticity and Quality
https://www.researchgate.net/publication/309521132_Pigments_in_Extra-Virgin_Olive_Oil_Authenticity_and_Quality
Pigments, divided into carotenoids and chlorophyll derivatives, are responsible for the colour of extra‐virgin olive oil (EVOO). The concentration of pigments in EVOO depends on several factors, such as the maturity of olives before oil production, the cultivar and the geographic origin of olives. Pigments naturally degrade in olive oil (OO) during storage, and they may decompose due to light, temperature and oxygen exposure.


#### Determination of Pigments in Virgin and Extra-Virgin Olive Oils: A Comparison between Two Near UV-Vis Spectroscopic Techniques
https://www.mdpi.com/2304-8158/8/1/18
The first method defines two indexes, K670 and K470, related to absorbance values of oil at wavelengths of 670 and 470 nm, respectively.


#### Sensing the Addition of Vegetable Oils to Olive Oil: The Ability of UV–VIS and MIR Spectroscopy Coupled with Chemometric Analysis
https://www.researchgate.net/publication/337771029_Sensing_the_Addition_of_Vegetable_Oils_to_Olive_Oil_The_Ability_of_UV-VIS_and_MIR_Spectroscopy_Coupled_with_Chemometric_Analysis

This study showed that both UV–VIS and ATR-MIR spectroscopy can detect levels of adulteration above 10% due to their lower error values in prediction. However, both methods have difficulties to detect low levels of adulteration (less than 1%).
Measured 200-800 nm.
Extra virgin Olive oil, peak at 670nm. And at 220 nm.

Using PCA, 2-3 compoents.
! nice plots.


#### Rapid adulteration detection of cold pressed oils with their refined versions by UV–Vis spectroscopy
https://www.nature.com/articles/s41598-020-72558-7
Measuring 350-850nm.
Converted the CIELAB, using a* and b* as features.
Quite linear response wrt percentages.

Absorbance spectra of cold pressed oils present a maximum at about 650 nm for all oils, and, except coconut oil, triplets at 450–500 nm36. These maxima do not appear in any of the refined oils.

#### Comparative Study Using Raman and Visible Spectroscopy of Cretan Extra Virgin Olive Oil Adulteration with Sunflower Oil
https://www.researchgate.net/publication/305924028_Comparative_Study_Using_Raman_and_Visible_Spectroscopy_of_Cretan_Extra_Virgin_Olive_Oil_Adulteration_with_Sunflower_Oil/figures?lo=1
We used both methods to study Cretan extra virgin olive oil adulterated with sunflower oil.
Statistical analysis based on partial least squares regression.
Visible spectroscopy had detection limits of 5.5% adulteration.

#### Rapid Detection of Fatty Acids in Edible Oils Using Vis-NIR Reflectance Spectroscopy with Multivariate Methods 
https://www.mdpi.com/2079-6374/11/8/261
This study was undertaken to establish a rapid determination method for quality detection of edible oils based on quantitative analysis of palmitic acid, stearic acid, arachidic acid, and behenic acid. Seven kinds of oils were measured to obtain Vis-NIR spectra.
The model of support vector machine (SVM) with standard normal variate (SNV) pretreatment showed the best predictive performance for the four fatty acids.
The results demonstrate that Vis-NIR spectroscopy combined with multivariate methods can provide a rapid and accurate approach for fatty acids detection of edible oils.
Measured 400-2500 nm.
Figure 4. The visualization of the quantitative results of four fatty acids in seven kinds of edible oils.

#### Reflectance Spectroscopy with Multivariate Methods for Non-Destructive Discrimination of Edible Oil Adulteration
https://www.mdpi.com/2079-6374/11/12/492

The visible and near-infrared (Vis-NIR) reflectance spectroscopy was utilized for the rapid and nondestructive discrimination of edible oil adulteration.
In total, 110 samples of sesame oil and rapeseed oil adulterated with soybean oil in different levels were produced to obtain the reflectance spectra of 350–2500 nm.

#### An RPi spectrophotometer distinguishes extra virgin olive oil from canola oil and light olive oil.
﻿https://hackaday.io/project/167360-pi-spectrophotometer-tests-olive-oil
Used a simple setup with diffration grating, LED, cuvette and camera without an enclosure.
The machine is capable of differentiating between extra virgin olive oil and canola oil.
Measures 350nm - 680 nm.
Custom software using TKinter.


#### Investigation the optical properties of Palestinian olive oils for different geographical regions by optical spectroscopy technique
https://www.sciencedirect.com/science/article/pii/S2772753X23004057
The first, peaking at 320 nm, was linked to polyphenols, the second, a red emission at 670 nm, to chlorophyll, and the third, spanning 400–580 nm, to oxidation products and vitamin E.
When examining olive oil adulteration with sunflower oil, both absorption and photoluminescence data exhibited a significant reduction in peak intensity for chlorophyll, carotenoids, and polyphenols. 

Extra virgin olive oils exhibit strong luminescence due to presence of chlorophyll.
To examine this phenomenon, we used UV Lamp with wavelength 365 nm and power 15 watt (Herolab GmbH- Germany).
Excitation-Emission Matrices (EEMs).

#### Characterization of extra virgin olive oils adulterated with sunflower oil using different physical methods
https://www.researchgate.net/publication/283296392_Characterization_of_extra_virgin_olive_oils_adulterated_with_sunflower_oil_using_different_physical_methods
Fluorescence spectra were measured using a fiber optic spectrometer (AvaSpec-2038, Avantes),
and the samples were excited by light emitting diodes at 370 nm, 395 nm, 425 nm and 450 nm using the set up.
The spectrometer’s sensitivity is in the (200 – 1100) nm range with a resolution of about 8 nm.


#### Analysis of Olive Oils by Fluorescence Spectroscopy: Methods and Applications
https://www.researchgate.net/publication/221923410_Analysis_of_Olive_Oils_by_Fluorescence_Spectroscopy_Methods_and_Applications

#### Predicting extra virgin olive oil freshness during storage by fluorescence spectroscopy
https://www.researchgate.net/publication/322316588_Predicting_extra_virgin_olive_oil_freshness_during_storage_by_fluorescence_spectroscopy
Highlight the possibilities of rapid spectrofluorimetric techniques for assessing oil freshness by checking the evolution of pigments during storage.
The best regression was obtained for 655 nm (adjusted-R2 = 0.91) wavelength, which matches the distinctive band of pigments. The two mathematical models described in this study highlight the usefulness of pigments in the prediction of the shelf-life of extra virgin olive oil.

Figure 4. Fluorescence spectra of eight virgin olive oil samples that range over the whole experiment of eighteen months of var. Hojiblanca at λ ex = 350 nm. The numbers in the spectra correspond to the month order during the experiment. Spectra from 400 nm to 700 nm.

#### Fluoresence Spectra From Vegetable Oils Using Violet And Blue Ld/Led Exitation And An Optical Fiber Spectrometer
https://www.researchgate.net/publication/263368577_Fluoresence_Spectra_From_Vegetable_Oils_Using_Violet_And_Blue_LdLed_Exitation_And_An_Optical_Fiber_Spectrometer
Figure 6. First derivative for (a) olive oils adulterated with sunflower oil and pomace olive oil and (b) extra virgin olive oils.

In this article the possibility to detect adulteration of costly olive oils with cheaper vegetable oils using fluorescence spectroscopy is studied. Total luminescence spectra were recorded by measuring the emission spectra in the range 350 nm to 720 nm for excitation wavelengths from 375 nm to 450 nm. Fluorescence spectra of 12 types of olive oil samples were studied. Ten of the olive oil types were purchased locally, while two (samples 1 and 4) were obtained directly from Greek olive oil producers.


#### Detection of Adulteration of Extra Virgin Olive Oil via Laser-Induced Breakdown Spectroscopy and Ultraviolet-Visible-Near-Infrared Absorption Spectroscopy: A Comparative Study 
UV-Vis-NIR absorption data, where all the EVOOs from each region are treated as one class, while the EVOO-edible oil mixtures are treated as four classes,
Measured 200-1000 nm. 350 - 750 nm.

#### Misc
(olive oil) excited with a violet laser at 405nm



## Light sources

High CRI LEDs. Above 90.
425nm-700nm.
4000k considered neutral.

CRI 93-95. 3030 seems like a good size.
https://www.digikey.no/en/products/filter/led-white-lighting/124?s=N4IgjCBcpgbGAWKoDGUBmBDANgZwKYA0IA9lANogBMYAzAAwCc9IxNtY9ArCALrEAHAC5QQAZSEAnAJYA7AOYgAvsThge0EGkhY8RUhRAMwjWlVZH6nBD2LH6CCPxDDREmQuXEAtOc3apAFd9MkhKHl4lFRBYZBBpABNRb04IQRFIEAshAE8BfFFMXDQooA


AW9523 GPIO Expander and LED Driver Breakout. QWIIC
https://www.adafruit.com/product/4886
8-bit linear constant-current LED dimming

SparkFun LED Driver Breakout - LP55231
https://www.sparkfun.com/sparkfun-led-driver-breakout-lp55231.html

I2C LED driver chips
https://www.digikey.no/en/products/filter/power-management-pmic/led-drivers/745?s=N4IgjCBcpgbFoDGUBmBDANgZwKYBoQB7KAbRACZYB2AFjAFYQDyBOGl8gDiYrY5Z6t6ABlgRmLemGE1Bk6fAn0AzGHG8VHOfSmyCIuDWE9lMliyonh9GlWMFT9MeR60at1%2B5rcCbzvZB3ZSpORRBaWh9w23YeTipYLQJ4xL0QFJYw%2BLs0%2BJZlAWSqNnU89zjimiz-ZTCOenIXAgtlTnULKqjpULA07sTGAm6qXp5uznJB8GFOCa6ZznKhhbaxleU12ZZ1br5NzIgAXQIABwAXKBAAZTOAJwBLADsAcxAAXyHaxmgQZEh0bD4IikdLCchgqb%2BcGUExObZRCawWB0VwsNr%2BVGcZSqVwNOhNcINVSyY4gc6XG4PF7vAgAWhcPz%2BdwArkDiJAyIxDh8QLSBIyoCy2SCjm8ed9QCcoGBTlLIJMefAfvcACaXWnSdTkyAgHgARzOAE9LtIAkaTjhLmgsMgxUA

## Linear CCD array

Toshiba TCD1304AP

Some, but limited selection at electronics component suppliers,

- DigiKey, https://www.digikey.no/en/products/filter/optical-sensors/image-sensors-camera/532?s=N4IgjCBcpgHAzFUBjKAzAhgGwM4FMAaEAeygG0R4AmAdhoBYA2EAXSIAcAXKEAZU4BOASwB2AcxABfIgFoqSEKkiCAroRLkQAVlaTpIZtBBCAJjxlgADBA7dIIEEQCOnAJ48rjkG-Z4eGHFQ9IA
- Mouser, https://eu.mouser.com/c/?type=CCD%20Linear%20Image%20Sensor&sort=pricing

- TCD1103GFG(8Z,AA2), 1.5k lines, 15 EUR
- TCD1209DG(8Z,K), 2k lines, 35 EUR
- TCD1304DG(8Z,K), 3k lines, 30 EUR
- EPC901-CSP32-033, 1k

TCD1304DG etc. Shows spectral response only from 400 nm. 20% point at 900 nm.

Some low resolution options, with serial readout.
Obsolete, but available?

- TSL1402R. 256 pixels. 
- TSL1410R. 1280 pixels. Obsolete, but available
- TSL1401CCS. 128 pixels Obsolete
- TSL1401. 128 pixels
Taken over by  

TSL1401. OBSOLETE, but available
https://www.digikey.no/en/products/detail/rochester-electronics-llc/TSL1401/12124933
320-1000 nm at 20%+ response. 128 pixels. 5 nm per pixel. Probably sufficient
DIP8. Serial readout.
5 USD.

#### Linear CCD module
https://hackaday.io/project/9829-linear-ccd-module
https://tcd1304.wordpress.com/

TCD1304-based linear CCD module driven by a Nucleo F401RE, an STM32F401 black pill or an STM32F103 blue pill
MCU can either be interfaced through SPI, UART or USB.

https://ottervis.wordpress.com/
OtterVIS LGL spectrophotometer.
The spectrometer’s sensor is a TCD1304 linear CCD.
Spectral range: 380-760nm
Resolution: ~2nm.
Framerate: 1hz.


#### TCD1304 USB Spectrograph Board
https://davidallmon.com/projects/adc0820-spectrograph

3694 pixel frame takes approximately 250mS to read, and download via USB

https://hackaday.com/tag/linear-ccd/

ESPROS epc901 CCD sensor.
1024 monochrome pixels.
Easy to interface with. Cost $24 USD.
2×16 0.5 mm pitch BGA
Open breakout boards - https://github.com/astuder/epc901 



## Scanning Monochromator Spectrometers

Use a single photodiode, a diffraction grating (or monochromator),
and a mechanical actuator (like a stepper motor) to scan the spectrum sequentially.

Photodiodes have a wider range of wavelengths compared to color CMOS camera sensors,
and also higher dynamic range.
Downside is of course the increased complecity of having moving parts.

IR-cut filter and use RGB Bayer filters limits cameras to ~400–700 nm.
Silicon photodiode might have as much as 190 - 1100 nm.
InGaAs photodiodes can cover 800 to 2600 nm.
https://www.learnabout-electronics.org/Semiconductors/diodes_27.php

Measurement diodes. Marktech MT03-023, 15 USD. 250nm - 1100 nm.

Generic. Wurth 1540051EA3590. OSRAM SFH 229. 400-1100 nm. 0.5 USD. 

Cheapest InGaAs.
Hamatsu G12183. Around 100 USD.
Marktech Optoelectronics. Has many options in 10 USD price range. Both 1700 nm and 2600nm.
Ex: MTPD2601N

NIR diffraction gratings around 100 USD.
https://www.edmundoptics.in/f/reflective-ruled-diffraction-gratings/12220/
By placing grating on a rotating pivot, can build a scanning monochromator?
Note that one also need to have mirrors.
Minimum is a focusing mirror and collimiating mirror?

#### TSP #38 - Teardown, Upgrade and Experiments with a Verity Visible Wavelength Monochromator
https://hackaday.com/2014/11/22/creating-a-scanning-monochromator/
https://www.youtube.com/watch?v=veETVeEsaNM
Shahriar upgrades a Verity visible wavelength monochromator model EP200Mmd,
to be able to perform automatic scans.
The instrument is retrofitted with a stepper motor and a microcontroller which performs wavelength scanning
between 225nm to 875nm.
The grating mirror is on a pivot, and the angle is changed using a linear actuator.


#### The Spinning Spectrometer
A different take on the good 'ol spectrometer: spinning the grating to get visible light spectra.
https://hackaday.io/project/8104-the-spinning-spectrometer
Using s single detector to record the wavelength.


Uses a slight curve on the diffraction grating.
To reduce blurring of spectral lines due to beam will diverge after diffraction.
Without uing a focussing lens or focussing mirror.
Got around 10nm resolution.

## Diffraction grating

Visible range most common.
300-700 nm.
For example 500 or 1000 lines per mm.

Can get in 2x2 inch sliding cards.
Or as a big roll.

#### TODO

- Design cuvette holder for Little Garden, for absorbation. WIP
- Setup Little Garden
- Create test samples of oils

Minituariszation

- Test on AS7343
- Implement in MicroPython, for running on ESP32 etc
- Design an LED driver board. I2C QWIIC pass-through.
Absorber source (white CRI93+), flouresence source


### AS7343
405-855 nm. 14 bands.
Pimoroni

https://shop.pimoroni.com/products/as7343-breakout?variant=41694602526803

Sparkfun.


## Little garden  spectrometer

Range. Possibly as wide as 340-1100nm.
However the response is very uneven at different wavelengths.
https://budgetlightforum.com/t/little-garden-spectrometer-impressions-opinions-discussion/225545

Hamamatsu C12880MA MEMS u-Spectrometer
https://www.hamamatsu.com/eu/en/product/optical-sensors/spectrometers/mini-spectrometer/C12880MA.html
https://groupgets.com/products/hamamatsu-c12880ma-mems-u-spectrometer
- Spectral response range: 340 to 850 nm
- Spectral resolution: 15 nm max.

Costs. $234.99 USD


### Wastewater analysis

Examples of Molecular UV/Vis Analysis of Waters and Wastewaters.

https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Analytical_Chemistry_2.1_(Harvey)/10%3A_Spectroscopic_Methods/10.03%3A_UV_Vis_and_IR_Spectroscopy

### Monochromatic camera

RP2040 Microcontroller Camera Development Board,
Onboard HM01B0 Grayscale Camera And 1.14inch IPS LCD Display
https://www.waveshare.com/pico-cam-a.htm

HM01B0. Ultra low power. 2mW at QVGA 30FPS.
Still has Bayer filter??

HM0360. Monochrome filter?
VGA resolution.
https://www.arducam.com/hm0360-vga-monochrome-dvp-camera-module-for-arduino-giga-r1-wifi-board.html
https://www.welectron.com/Arducam-B0336N-HM0360-VGA-CMOS-Monochrome-Camera-Module-NoIR-for-RP2040-Arduino_1
Quantum efficiency. 40% at 800 nm. 8% at 1000 nm.
Seems pretty bad?
Unspecified below 400 nm.

#### Cuvettes

10 mm light path is standard.
They are 12.5 x 12.5 mm outer size, 45 mm tall.

https://www.frederiksen-scientific.no/produkt/kyvette-uv-mikro-100-stk/545150

https://www.fybikon.no/kjemi/kjemisk-analyse/kromatografi-og-spektroskopi/kuvette-standard-pk-100-stk-inkl-20-stk-lokk
https://www.fybikon.no/kjemi/kjemisk-analyse/kromatografi-og-spektroskopi/kuvettestativ-for-10-kuvetter

UV cuvettes much more expensive?


##  Go Direct® Spektrofotometer, SpectroVis Plus

600 USD. 9000 NOK

https://www.fybikon.no/biologi/dyr-og-planter/fotosyntese-og-celleaanding/go-direct-spektrofotometer-spectrovis-plus

380-950 nm, 4 nm resolution

500nm and 405 nm exitation sources

## Open source software

#### spectro-web

Spectrometer using camera. Runs entirely in web browser
https://github.com/gheja/spectro-web

#### Theremino_Spectrometer

https://www.theremino.com/en/downloads/automation#spectrometer

https://www.theremino.com/en/downloads

#### PySpectrometer

https://github.com/leswright1977/PySpectrometer2
https://github.com/leswright1977/PySpectrometer


