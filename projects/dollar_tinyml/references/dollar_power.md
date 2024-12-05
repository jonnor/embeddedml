
# Sub 1 dollar power

Consumable battery

- CR1216 battery at 0.2 USD
- CR2477 `0.8 USD @ 1k`

Rechargable battery

- LIR1220 `0.2 USD @ 1k`. 7 mAh
- Battery charger `0.05 USD @ 1k`
 
## Lipo battery chargers

Many options below 0.1 USD
https://www.lcsc.com/products/Battery-Management-ICs_612.html?keyword=battery%20charger

Typically in SOT23-5 package.
Seems like they are clones of LTC4054 from Linear.

Examples: GX4054, LTH7R, LR4054A-T
3000 pcs reel down to 33 USD.

English datasheets. LP4054H, PJ4054B
Still under 0.05 USD @ 1k.

## Lipo battery protection

Fully integrated undervoltage "overdischarge".

- JSMSEMI DW06. 0.05 USD
- DW03. 0.04 USD

Semi-integrated. Needs external NMOS

- DW01 


## Supercapacitors

Lithium Ion Capacitors 15F 3.8v can be had for 32 cent @ 1k.
Example: SLA3R8L1560613 at LCSC.

Ceramic SMD typically up to 100 uF.
Alu electrolytic typically up to 1000uF, 2-5 cent @ 1k.

## Energy harvesting

Piezoelectric.
In footwear. For example in an insole. Might be possible to get 1mW.
Walking frequency might be around 1 Hz.
1 mF needed to last 60 seconds with 100 uA current draw, from 3.0 to 2.0 V.

Would ideally want circuit to work also when not walking,
some minutes or hours.


https://www.mdpi.com/2079-9292/12/6/1278
NRF51 beacon down to 12 uA average with 4 second advertising interval.

> Due to the low internal resistance of the Peltier module with the use of an appropriate conditioning system,
> temperature differences of several Kelvin are sufficient to power the beacon
> 
> With temperature differences less than 70 K, the voltage obtained from the cell is low compared to the nominal voltage of the beacon.
> The higher the temperature difference, the closer the voltage on the Peltier module is to the nominal voltage of the transmitter...
> With a temperature difference of 70 K, the Peltier module generates enough voltage to power the beacon directly.


### Energy harvesting controllers

SPV1050.
For thermoelectric generators. Or solar panel.


AEM30940

LTC3108. For thermoelectric.
Breakout boards exist with room for transformer.
A 40mm x 40mm TEG (with <2.5Ω source resistance) with a dT of 10°K across it will produce about 4mW.

BQ25570. bq25505. bq25504. For TEG thermoelectric.

LTC3588. For vibrating piezo. Or solar panel.
Highly integrated.
Adjustable output voltage. Power-good checks.
Can be used with regular capacitor. 
Supports backup battery.
Breakouts available.

### Piezeoelectric vibration harvesters

MIDE V21BL.
Some 2-3 inches long. Using 0-15 gram weights. Designed for AC motors.
Can collect up to 1 mW.
