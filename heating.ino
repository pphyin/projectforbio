
int pwm_value = 0;
String inString = "";
int PulsePin = 9;
int heatPin=8
void setup() {
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {
    while (Serial.available() > 0) {
      int inChar = Serial.read();
      Serial.print("Heatingcurrent")
       analogRead(heatPin);
      if (isDigit(inChar)) {
        // convert the incoming byte to a char and add it to the string:
        inString += (char)inChar;
      }
      // if you get a newline, print the string, then the string's value:
      if (inChar == '\n') {
        pwm_value = inString.toInt();
        analogWrite(PulsePin, pwm_value);
       
        Serial.print("PWM Value:");
        
        Serial.println(pwm_value);
//        Serial.print("String: ");
//        Serial.println(inString);
//        analogWrite(PulsePin, inString.toInt());
        // clear the string for new input:
        inString = "";
      }
    }
  }
}
