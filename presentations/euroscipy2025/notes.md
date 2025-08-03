
## Concept

Focus on scientific application of (IoT) sensor-nodes,
and how they are used.
Highligh how this can be implemented using emlearn + MicroPython.

## The talk

Wednesday, August 20, 1:30 PM
Room 1.19 (Ground Floor)
Computational Tools and Scientific Python Infrastructure



## Outline

See also [proposal.md](./proposal.md)

Broad categories

- Scientific applications
- Sensor nodes and Wireless Sensor Networks
- About MicroPython
- Tools and practices for efficient sensor data processing in MicroPython

## Planning

### About MicroPython
Pick from existing presentations. Ex FOSDEM.

### Tools and practices for efficient sensor data processing in MicroPython
Pick from PyConZA presentation

### Sensor nodes and Wireless Sensor Networks

Existing slide(s)

- ML-powered sensor node. Architecture
- Microcontrollers, what are they.

Add a bit more.
Especially things that make later parts more relevant.

- Wireless sensor networks. Principle. Deployed in a large area.
Communication to a central point. Via gateway or not.
Non-connected loggers. Storing to SDcard etc. Hybrid, raw data on SD.
- Common wireless protocols.
Typical ranges. Typical data rates. Typical power.
Could be in terms of "typical architectures"?
Motivation for ML on edge: Being able to transmit
- MEMS sensors ? Could be covered under applications also
- Batching of data. Very beneficial. Reducing wakeup times.


####  WiFi
Very easy. Very well supported.
Not power efficient. WiFi 6 improves


#### Cellular
LTE CAT M1 / LTE CAT NB "narrowband iot"
PPP over Serial (PPPoS)
machine.PPP 
https://docs.micropython.org/en/latest/library/network.PPP.html

#### BLE
Ex to mobile phone, or gateway
! NRF52 not so well supported right now.
Zephyr port is improving this.
One of the best low-power BLE chips.
ESP32 not that low power

#### LoRa
LoraWAN.
Public network like ThingsNet
Private network using gateways
https://github.com/micropython/micropython-lib/tree/34c4ee1647ac4b177ae40adf0ec514660e433dc0/micropython/lora
Support bunch of the most common modules from Semtech SX1262 

- Duty cycle limits: EU has 1% duty cycle restriction (36 seconds/hour transmission time)
- Fair Access Policy: TTN limits to 30 seconds uplink airtime per device per day
- Typical use: Most applications work well with 10-50 byte payloads sent every 15-60 minutes
- Recommendation: Use SF7-SF9 with 20-50 byte payloads

airtime calculator
https://www.thethingsnetwork.org/airtime-calculator
51 bytes SF7, 125 khz, EU686. 118 ms.
With 30 seconds daily, 11 per hour avg
5 minute interval
Might need to go down to 1/2 of this

LoraWAN packet overhead. 13 bytes minimum ?
EU868 SF12: 51 bytes max → 38 bytes application data

Confirmed ACK in LoRaWAN:
Set ADR bit in FCtrl to request confirmation
Device sends uplink with "confirmed" flag
Network server responds with downlink ACK
If no ACK received, device retransmits (up to 8 times default).

Coverage on public network
https://www.thethingsnetwork.org/map
Krakow has 3 gateways nearby conference center
Oslo have

#### Thread
IP-based. 6LoWPAN / IEEE 802.15.4.
Zigbee uses same transports.



### Scientific applications

- Ecology
- Biology?
- Animal husbandry, livestock
- Agriculture, farming
- Human health

#### For sound

Usecases

- Understanding wildlife behavior
- Illegal logging detection
- Noise monitoring

Tasks

- Birdsong detection & classification
- Dolphin/whale

#### For accelerometer

Usecases

- Sleep quality tracking
- Monitoring cows/sheep

Tasks

- Human Activity Detection
- 

#### For image

- Wildlife cameras

#### Other


