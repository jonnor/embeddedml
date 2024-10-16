

#include "model.h"

class LightSensorLed {

public:
  LightSensorLed(int writePin, int readPin);

  void start();
  int stop();

public:
  int nPin;
  int pPin;
  int startLevel;
};

LightSensorLed::LightSensorLed(int _nPin, int _pPin)
{
  nPin = _nPin;
  pPin = _pPin;
  startLevel = -1;
}


void LightSensorLed::start()
{
  // Apply reverse voltage, charge up the pin and led capacitance
  pinMode(nPin, OUTPUT);
  pinMode(pPin, OUTPUT);
  digitalWrite(nPin, HIGH);
  digitalWrite(pPin, LOW);

  // Isolate the pin 2 end of the diode by changing it from OUTPUT HIGH to 
  // INPUT LOW (high impedance input with internal pull-up resistor off)
  pinMode(nPin, INPUT);
  digitalWrite(nPin,LOW);  // turn off internal pull-up

  startLevel = analogRead(nPin);
}

int LightSensorLed::stop()
{
  if (startLevel < 0) {
    return -1;
  }
  const int level = analogRead(nPin);

  const int change = startLevel - level;
  return change;
}



LightSensorLed sensorG(A0, 2);
LightSensorLed sensorR(A1, 3);
LightSensorLed sensorB(A2, 4);

const int buttonPin = 11;
const int ledIndicatorPin = LED_BUILTIN;

void setup()
{
  pinMode(ledIndicatorPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); 
  
}

void
measureLight(int rgb[3], int milliseconds)
{
  LightSensorLed *sensors[] = {
    &sensorR,
    &sensorG,
    &sensorB,
  };
  for (int i=0; i<3; i++) {

      LightSensorLed *sensor = sensors[i];
      sensor->start();
      delay(milliseconds);
      const int value = sensor->stop();
      rgb[i] = value;
  }

}

static const char *class_names[] =
{
  "Other",
  "Purple",
  "Yellow",
};

void loop()
{

  static int64_t lastRead = 0;
  const int samplerate = 2;
  const int samplePeriodMs = 1000/samplerate;
  const int64_t tick = millis();

  const int sampleTime = 100;

  if (tick >= (lastRead + samplePeriodMs) ) {
    lastRead = tick;

    // check button
    // XXX: not ideal way to check button, is delayed by the (blocking) light measurement
    // but it means we do not need separate rate limiting
    const bool buttonPressed = digitalRead(buttonPin) == LOW;
    digitalWrite(ledIndicatorPin, buttonPressed);

#if 1
    // log button state
    Serial.print("button,");
    Serial.print((long int)tick);
    Serial.print(",");
    Serial.println((int)buttonPressed);
#endif

    // sample
    int rgb[3] = {-1, -1, -1};
    measureLight(rgb, sampleTime);

#if 1
    // log sensor data
    Serial.print("val,");
    Serial.print((long int)tick);
    Serial.print(",");
    Serial.print(rgb[0]);
    Serial.print(",");
    Serial.print(rgb[1]);
    Serial.print(",");
    Serial.println(rgb[2]);
#endif

#if 1
    // Run detection model
    float features[3];
    features[0] = rgb[0];
    features[1] = rgb[1];
    features[2] = rgb[2];
    const int32_t predicted = simple_rgb_pink_yellow_other_predict(features, 3);
    const char *predicted_class = "ERROR";
    if (predicted >= 0) {
      predicted_class = class_names[predicted];
    }
    Serial.print("predict,");
    Serial.print((long int)tick);
    Serial.print(",");
    Serial.print(predicted);
    Serial.print(",");
    Serial.println(predicted_class);
#endif

  }


}
