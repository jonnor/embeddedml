

# Carbon rod microphone
The carbon rod microphone was one of the first designs.
Predates the carbon granula "button" microphone.

Principle: The loose contact between two objects is such that when vibrations occur,
the surface resistance changes. An electrical current is passed through, and a voltage variation appears.
Carbon is practical because it does not oxidice,
and provices an inherent resistance.

## References

#### Crowhurst
http://www.vias.org/crowhurstba/crowhurst_basic_audio_vol1_035.html
Carbon rod vertically, loosely held between two plates 

#### Popular Science 1945
https://onetuberadio.com/2015/11/23/science-fair-idea-homemade-microphones/
references November 1945 issue of Popular Science.
Microphone is made using 3 nails, 1 positioned on top of two others, on a sounding board.

#### Simplifier: Compound, high quality wooden microphone
https://simplifier.neocities.org/compound
Speech sounds pretty good! Clear and OK frequency balance. A bit boxy/resonant.
Uses a thin wood sheet as a diaphram.
Uses 4 carbon rods suspeneded between 2 carbon terminals.
Rods are connected 2 in series, 2 in parallell.

! Good contender for making a 3d-printed replica.

#### Simpifier: Carbon, simple wood plank microphone
https://simplifier.neocities.org/carbon
Diaphragm is a piece of pine board,
with a 3 by 3 inch section milled down to a thickness of 1/16th of an inch (1.6 mm).
The loose contact is made between two pieces of 1/4 inch graphite rod.
AC modulation 10mA p2p with normal speaking voice.
Used single D cell battery, 1.5 V. 80 mA quistent current. Voice modulates of 5-20 mA.
Used 5K:8 audio transformer in reverse, to get up to 3Vpp.

Double sided tape to attach carbon rods.

# Testing

### Second iteration
March 16, 2024

Designed conductive parts to be 3d-printed.
Using ProtoPasta Conductive Graphite filament. PLA based.
Printing at 0.20mm with 205 deg C failed. Lots of areas with critical underextrusion.

Tried printing at 0.16 mm with 215 deg C.
Results were ??

Issue: holder can rotate. Will be hard to hold both carbon rods equally.
Use double slots? Allows adjustment and should at least be stable after set.
Rods are a bit long. When glued to center, at least need more adjustment downwards to be able to insert.
Could make slight adjustment also to the holder, moving the screw hole up.

Also added a stand. 


### First test
Jan 01, 2024.

Printed parts for a single grafite rod.
Fits on back of a 90mm diagrapm ring.

Using a 3.7v 200 mAh lipo battery.
Just cause did not have a holder for any 1.5V cells.
Around 50 mA bias current.
Connected directly to computer input via 3.5 mm TRRS.

It makes sound, but sound quality is pretty bad.
Can barely make out the words in the speech.
And very easy to create crackles. Possibly from unintended motion.

A very weak point is the attachment of the graphite rods.
Using double sided tape and it is not really cutting it...
The hanging rod can rotate a lot from side to side. Maybe glue would fix it.
There is a bit of tension on it from the copper wire.
The rod on diaphram tends to squueze out of its slot. Glue will probably do the trick.
The pivots slides sideways a bit. Probably easy to fix by printing it longer.

Usage and testing would benefit a lot from having direct feedback in headphone.
A stand would also be useful to reduce influence of moving hands.
Putting it on top of a box to get a practical high for speech would also help in testing distances/angles etc.

Pivot rotates very nicely.
Printed diaphram seems to work nicely.
0.4mm migth be a bit thin. Could be that going to 0.8mm or similar will be better.

# Improving quality

Weaknesses

- Crackling when overloaded 
- High static noise. Very apparent when no-one is speaking.
- Frequency response. Probably not ideal?
- Sensitivity to handling noise.

Ideas for improving

- Pop filter. To reduce plosives
- Static removal with spectral substraction. Constant or VAD activated
- Frequency compensation. Constant or VAD activated
- Adaptive corrections of crackling. RNNoise style
- Multiple. 2S2P used in Simplifier Compound
- Appropriate selection of bias current.
Might not matter much if kept in a sane range. Sub 100 mA?
- Appropriate geometry of contacting surfaces.
Simplifier Compound uses conical shapes - is that beneficial?

#### Spectral subtraction
https://abhipray.com/posts/sigproc/classic_speech_enhancement/spectral_subtraction/


"Enhancement of speech corrupted by acoustic noise",
Proceedings of the International IEEE Conference on Speech, Acoustics and Signal Processing,
p208-211, 1979.

### Deep Speech Enhancement

https://github.com/Rikorose/DeepFilterNet



# Carbon powder microphone

#### Exploratorium Teacher Institute: Carbon Charcoal Microphone
https://www.youtube.com/watch?v=uAnlmoei_Co

Uses grafite powder.
Two plastic cups to put it in between.
Conductive aluminium tape for leads.

# Button microphone

Invented around 1920.

#### Duffy P. Weber, Building a 3D Printed Double-Button Carbon Microphone
https://www.youtube.com/watch?v=8nSSCG2xCac

Used activated charcoal granulas as a base.
Ground it into finer powder using a hammer and filtered with a metal mesh.

A comparison with an original metal double button carbon microphone is performed.
Works, but sound quality is not that great.
Author provides a number of areas that improvements can target.

# Matchbox microphone

Many videos showing this on Youtube.
Sound quality tends to be pretty bad however.
Thin 0.5mm rods do not work - need a grafite stick from pencil.
Many recommend sanding the connecting surfaces flat.
Some just let the top electrode lie on top of the others - cannot be moved around.
Others led the top be tensioned slightly across the others - can be moved.

## Tests

Pencil lead is approximately 2-2.5 mm diameter.

Pencil lead resistance.
Approx 3 ohms when measured 3 mm apart.
And approx 8 ohms when measured 80 mm apart.
Seems that surface resistance is large.

9V over 8 ohms would lead to over 1 amp of current.
Seems excessive. One or two 1.5V battery might be better suited.
Maybe reduces potential of arcing?

## References

#### Over Engineered: How to make a Microphone
https://www.youtube.com/watch?v=r7s_P2opjX0

First microphones, late 1800s.

Uses a frame to have a graphite lead that dangles down.
Diaphram of thin plastic connected to a little rod, with a graphite lead at the end.
Seems slightly better than plain matchbox designs.

9V battery used for power.
Used a transformed to amplify and isolate the AC.
Might also work without transformed, just using a capacitor instead.

Changing angle of frame adjust sensitivty by the "pretension" between the grafite sticks.
Would probably benefit from the 2-series, 2-parallel scheme from the "compound" mic.

# Dynamic microphone

How to Build a DIY Dynamic Microphone With Some Wire and a Magnet
https://www.youtube.com/watch?v=94A7uzaGct8

Very DIY build. Out of a CD etc.

