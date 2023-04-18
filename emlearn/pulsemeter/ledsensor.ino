#define LED_N_SIDE 9
#define LED_P_SIDE 8

void setup()
{
  
  
}

// Code based on
// https://playground.arduino.cc/Learning/LEDSensor/
void loop()
{
  unsigned int j;

  // Apply reverse voltage, charge up the pin and led capacitance
  pinMode(LED_N_SIDE, OUTPUT);
  pinMode(LED_P_SIDE, OUTPUT);
  digitalWrite(LED_N_SIDE, HIGH);
  digitalWrite(LED_P_SIDE, LOW);

  // Isolate the pin 2 end of the diode by changing it from OUTPUT HIGH to 
  // INPUT LOW (high impedance input with internal pull-up resistor off)
  pinMode(LED_N_SIDE, INPUT);
  digitalWrite(LED_N_SIDE,LOW);  // turn off internal pull-up resistor

  // Count how long it takes the diode to bleed back down to a logic 0 at pin 2
  const int microsPerCycle = 10;
  for ( j = 0; j < 60000; j++) {
    if ( digitalRead(LED_N_SIDE)==0) break;
    delayMicroseconds(microsPerCycle);
  }
  const int delayMs = ((int64_t)microsPerCycle * j) / 1000;
  // You could use 'j' for something useful, but here we are just using the
  // delay of the counting.  In the dark it counts higher and takes longer, 
  // increasing the portion of the loop where the LED is off compared to 
  // the 1000 microseconds where we turn it on.

  Serial.print("cycles: ");
  Serial.println(delayMs);

  delay(100);
}
