/*
SERVO CALIBRATION SCRIPT - Michael Feldkamp, ME 8284, Originally written December 2024
GITHUB: https://github.com/noesantib1999/ICE_ICE
Purpose: This script directly controls the positions of each servo for use in initial hardware assembly and troubleshooting.
Implementation: Servos are initially moved to "servo_center_pos" defaulting at 135 degrees. Script will then accept serial inputs to control servo position via the following format:
                "Axx" will set the Anterior-Posterior (AP) servo to the float value xx.
                "Ryy" will set the Left-Right (LR) servo to the float value xx.
                Should accept only one input at a time. Any other input formats will be ignored.
Instructions: 
  General:  Ensure that servos are connected to power and their respective pins. Connect the Teensy to a computer establishing a USB connection.
  Assembly: Prior to assembling the ICE hardware, ensure servos can spin freely and positions are set to 135 using this script. Assemble servo gear interface with the ICE
            catheter in its home position (completely straight). Once assembled, ensure servos can spin by setting the position to a slightly different value using the above format.
            Progressively test values closer to both 0 and 270 and identify the furthest distance the servos can spin from the home position. Use this to update "servo_pos_limit" for
            both this script and "TEENSY_INTERFACE."

*/

#include <Servo.h>

// Pin definitions:
#define servo_AP_pin 35
#define servo_LR_pin 36

// System definitions:
#define servo_pos_limit 80 // Maximum amount servo should turn in a given direction in degrees, max is 135
#define servo_center_pos 135 // Servo position when catheter is straight

Servo servo_AP;
Servo servo_LR;

float cmd_Pos_AP = 0;
float cmd_Pos_LR = 0;

float setServoPos(Servo &servoObj,float cmdPos){
  //cmdPos is in degrees. This needs to be constrained and then remapped to microseconds
  float cmdPos_constrained = constrain(cmdPos,servo_center_pos-servo_pos_limit,servo_center_pos+servo_pos_limit); //Constrains the command degrees to center +- limit
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

  servo_AP.attach(servo_AP_pin,500,2500);
  servo_LR.attach(servo_LR_pin,500,2500);

  // Put both servos to middle position
  cmd_Pos_AP = setServoPos(servo_AP,servo_center_pos);
  cmd_Pos_LR = setServoPos(servo_LR,servo_center_pos);

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
  Serial.println("***************");
}
