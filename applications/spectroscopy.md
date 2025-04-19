
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

#### TODO

- Order cuvettes
- Design cuvette holder for Little Garden, for absorbation. Incandecent bulb
- Setup Little Garden
- Create test samples of oils

Minituariszation

- Order AS7343, from Pimoroni
- Test on AS7343
- Implement in MicroPython, for running on ESP32 etc
- Design an LED driver board. I2C QWIIC pass-through. Absorber source (white CRI93+), flouresence source


### AS7343
405-855 nm. 14 bands.
Pimoroni

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
