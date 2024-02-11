
# Development board sent to production

I made an initial development board.
This supports both sound-based and accelerometer-based ML tasks.

- Microcontroller. Puya PY32F003
- BLE beacon transmitter
- Accelerometer. ST LIS3DH
- Microphones. Top-port or bottom-port MEMS, or external electret
- Battery charger for LiPo/Li-Ion cells
- USB Type A connector for power/charge

Using a pre-built and FCC certified module for Bluetooth Low Energy, the Holtek BM7161.
This is a simple module based around the low cost BC7161 chip.

An initial batch of 10 boards have been ordered from JLCPCB.

Also did a check of the BOM costs.
At 200 boards, the components except for passives cost

With microphone: 0.66 USD per board
With accelerometer: 0.825 USD per board

Additionally there are around 20 capacitors, 1 small inductor, and 20 resistors needed.
This is estimated to be beween 0.15-0.20 USD per board.
So it looks feasible to get below the 1 USD target BOM, for as low as 200 boards.



