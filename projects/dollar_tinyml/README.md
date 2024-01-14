
# 1 dollar TinyML

A computer with a modern GPU for machine learning is approx 1000 USD.
The state-of-the-art ML models that in the mainstream attention are getting ever larger.
Currently being led by Large Language Models and Generative Image models.
Requiring more compute and RAM every year.

TinyML is a whole nother beast
- with a focus on tiny models that can run on small,power-efficient and low-cost microcontrollers.
Low cost enables massive scale.

Taking this to an extreme, this project raises the question

> Can one build a whole TinyML enabled sensor for under 1 USD?

## Current status

**Feasibility research done. Prototyping hardware+software**.

- Initial system architecture decided. See below
- Feasibility research documented under [references](./references)

See also [TODO](./TODO.md)

## Scope and limitations

We consider total costs as the Bill-of-Materials (BOM) for a useful system.

- The system must perform a useful function
- System should be able to work stand-alone
- Reliance on external items must be limited to items that any consumer can be expected to have already
Example: smartphone, USB charger, PC
- PCB Assembly (PCBA) costs are not included
- Mechanical elements apart from PCB not included
- Assuming production volume of 1000 units


## System architecture

Key functionality

- Capture and process motion/vibration data (from accelerometers)
- Capture and process audio data (from microphone)
- Running classification algorithms such as decision tree ensembles and recurrent neural networks
- Transmit results using BLE advertisements

Example usecases

- Human Activity Detection
- Sound Event Detection
- Voice/Speech Activity Detection

Components

```
Microcontroller                 PY32F003A
MEMS accelerometer.             ST LIS2DH12
MEMS microphone (analog)        LinkMEMS LMA2718
Bluetooth Low Energy beacon     Holtek BC7161
Battery                         LIR1220, charger included
External power                  USB Type A (PCB edge connector)
```

BOM for core components `0.90 USD`.
This leaves `0.10 USD` for jellybeans (standard capacitors/resistors).
Possible to drop either the microphone+opamp (0.12 USD) or accelerometer (0.26 USD).
Should also be possible to drop the battery (0.25 USD), if running on USB power.

[Bill of Materials](hardware/dml10/BOM.csv).

## Related projects

[emlearn](https://emlearn.org), a Machine Learning engine in C99, designed for tiny microcontroller and embedded systems.


