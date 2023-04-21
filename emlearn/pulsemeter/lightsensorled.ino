


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




LightSensorLed sensor(A1, 8);

void setup()
{
  
  
}


void loop()
{

  static int64_t lastRead = 0;
  const int samplerate = 20;
  const int samplePeriodMs = 1000/samplerate;
  const int64_t tick = millis();

  if (tick >= (lastRead + samplePeriodMs) ) {
    lastRead = tick;

    int val = sensor.stop();

    if (val >= 0) {
      // do something with data
      Serial.print("value ");
      //Serial.print((long int)tick);
      Serial.print(",");
      Serial.println(val);
      
    } else {
      // before first measurement cycle
    }

    sensor.start();
  }

}
