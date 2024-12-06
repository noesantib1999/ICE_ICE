#include <Servo.h>

// Pin definitions:
#define servo_AP_pin 13
#define servo_LR_pin 14

#define servo_pos_limit 135 // Maximum amount servo should turn in a given direction in degrees, absolute max is 135
#define servo_center_val 135 // Servo position when catheter is straight

Servo servo_AP;
Servo servo_LR;

float cmd_Pos_AP = 0;
float cmd_Pos_LR = 0;

float setServoPos(Servo &servoObj,float cmdPos){
  //cmdPos is in degrees. This needs to be constrained and then remapped to microseconds
  float cmdPos_constrained = constrain(cmdPos,servo_center_val-servo_pos_limit,servo_center_val+servo_pos_limit); //Constrains the command degrees to center +- limit
  int cmdPos_micros = map(cmdPos_constrained,0, 270, 500, 2500); // The servo operates between 0 and 270 degrees for 500-2500 microseconds
  servoObj.writeMicroseconds(cmdPos_micros); // Using microseconds instead of regular servo.write() due to servo functionality;
  return cmdPos_constrained; // Rewrite the command position to the constrained position.
}

void handleSerialInput(float* cmd_Pos_AP, float* cmd_Pos_LR){
  while ( Serial.available() ){
    int inByte = Serial.read();
    switch (inByte) {
      case 'A':
        *cmd_Pos_AP = Serial.parseFloat();
        Serial.print("AP set to "); Serial.print(*cmd_Pos_AP); Serial.print("\n");
        break;
      case 'R':
        *cmd_Pos_LR = Serial.parseFloat();
        Serial.print("LR set to "); Serial.print(*cmd_Pos_LR); Serial.print("\n");
        break;
      default:
        Serial.println("ERROR: Failed to parse input");

    }
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("Serial connected, running initial setup: ");
  delay(500);

  servo_AP.attach(servo_AP_pin);
  servo_LR.attach(servo_LR_pin);

  // Put both servos to middle position
  cmd_Pos_AP = setServoPos(servo_AP,servo_center_val);
  cmd_Pos_LR = setServoPos(servo_LR,servo_center_val);

  Serial.println("Now accepting commands: ");
  delay(500);
  Serial.clear();
}

void loop() {
  delay(10);
  handleSerialInput(&cmd_Pos_AP, &cmd_Pos_LR); // Adjust servo position command using this function. Commands must be 0-270 based on our current servo

  cmd_Pos_AP = setServoPos(servo_AP,cmd_Pos_AP);
  cmd_Pos_LR = setServoPos(servo_LR,cmd_Pos_LR);

  Serial.print("AP_Pos:"); Serial.println(cmd_Pos_AP);
  Serial.print("LR_Pos:"); Serial.println(cmd_Pos_LR);
  Serial.println("***************")
}
