
# Applications

Notes on various applications of embedded ML / TinyML that are quite established.

- [Human Activity Recognition](./human-activity-recognition.md)
- [Gesture recognition](./gesture-recognition.md)
- [Battery Health estimation](./battery-health.md)
- [Fall detection](./fall-detection.md)

# Potential future applications

[How ML/DL is Disrupting Sensor Design](https://drive.google.com/file/d/0BzrlDxVZWSUpbkZrRnlMbmE2c2s/view).
Compressed sensing. Random projections.

[Rise of the super sensor](https://www.computerworld.com/article/3197685/internet-of-things/google-a-i-and-the-rise-of-the-super-sensor.html).
CMU has developed a generic 'synthetic sensor', using audio/vibration etc.
"the revolution is to install a super sensor once, then all future sensing (and the actions based on that sensing)
is a software solution that does not involve new devices"

Soft Robotics.
[Youtube video about easy-to-construct soft gripper with integrated resistive sensors](https://www.youtube.com/watch?v=BLE5yhS3k3I).
Could train algorithms to detect objects gripped.

## Existing projects

Interesting projects realized using embedded machine learning / TinyML.

* [RPS-RNN](https://github.com/PaulKlinger/rps-rnn).
Small physical device that can play Rock, Paper, Scissors slightly better than chance.
Custom electronics and 3d-printed casing.
3-layer RNN running on 8-bit microcontroller, Attiny1614.

