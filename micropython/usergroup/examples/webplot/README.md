
# Plotting data in browser

## Dependencies

- ESP32 or RPI Pico/Pico2 W
- Flash [MicroPython](https://micropython.org/download/) to your device
- Download and install [MicroDot](https://github.com/miguelgrinberg/microdot)

## Run

NOTE: configure the WiFI credentials SSID/PASSWORD

Copy files across
```
mpremote cp index.html data.csv :
```

```
mpremote run webplot.py
```
