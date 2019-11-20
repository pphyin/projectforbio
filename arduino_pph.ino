
#include <Wire.h>


const int RECEIVE_REGISTER_SIZE = 8;
const int SEND_REGISTER_SIZE = 8;
float receive_registers[RECEIVE_REGISTER_SIZE];
float send_registers[SEND_REGISTER_SIZE];
int current_send_register = 3;


int DO_KALMAN_UPDATE_COMMAND = 100;
int STRING_COMMAND = 10;
int UPDATE_SEND_REGISTER = 11;
// This is the code that is run when first downloaded to the Arduino. It is called once and sets up many
// important environments and variables for the Arduino
void setup() {
  //Initiate Serial communication. It's good practice to always do this in Arduino
  Serial.begin(9600);

  // join i2c bus with address #8
  Wire.begin(0x8);     

  // tell the slave device what it should do when the master sends it data
  // receiveEvent needs to be a method with a void return type and a single parameter
  // of type int that indicates how many bytes are being written (this includes the command byte)        
  Wire.onReceive(receiveEvent); 

  // tell the slave device what it should do when the master asks for data. Since the master won't send
  // a command saying what data it wants, you will need to get creative in order to send the master
  // different kinds of data
  Wire.onRequest(sendData);

  
}

// This function is looped continuously. After calling setup, Arduino essentially runs while(True){ loop(); }
void loop() {
  // for now do nothing
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  String full_datastring = "";
  
  while (Wire.available()) { // loops through all the bytes that are sent over the wire
    // read in the information on the wire one byte at a time.
    // c can be set to any one byte primitive type such as char, int, byte. This type will cause c to be treated differently
    char c = Wire.read(); 
    full_datastring = full_datastring + c;
  }
  // extract the command byte based on the command byte have different behavior
  byte command = full_datastring.charAt(0);

  // read in a string and interpret data as string
  if(command == STRING_COMMAND)
  {
    Serial.println("received data string");
    String data = full_datastring.substring(1);
    Serial.println(data);
  }

  // called before the Pi reads from a register in send register. Updates which register the
  // Pi will read from.
  if(command == UPDATE_SEND_REGISTER){
    int data = full_datastring.substring(1).toInt();
    current_send_register = data;
    Serial.println("updating send register");
    Serial.println(current_send_register);
  }

  // Pi can trigger commands by sending a command byte mapped to a command
  if(command == DO_KALMAN_UPDATE_COMMAND)
  {
    kalman_update();
  }

  // If the command is inside the default write register range then write to the write register
  if(command >= 0 && command <= RECEIVE_REGISTER_SIZE)
  {
    // received a float and therefore write to a register
    Serial.println("Received Data Float. Writing to register " + String(command));
    float data = full_datastring.substring(1).toFloat();
    Serial.println(data);
    receive_registers[command] = data;
  }
   
  // Take care not to continue calling Wire.read() if there is nothing on the wire as you will get nonsense typically
}

// function that exectures whenever the master requests it. This function cannot have any parameters, and so
// you will need to take care in order to have the function write different types of information to the master
// one suggestion is to send a command from the master to the slave telling it what data you want and then having the Arduino write it
void sendData() {
  // send the data to the master
  char data[8];
  dtostrf(send_registers[current_send_register],8, 4, data);
  Serial.println(data);
  Wire.write(data);
 
}

void kalman_update() {
  Serial.println("doing kalman update");
}






  
