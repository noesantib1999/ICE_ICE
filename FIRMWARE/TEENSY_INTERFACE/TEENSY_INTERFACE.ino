/*
TEENSY INTERFACE SCRIPT - Michael Feldkamp, ME 8284, Originally written December 2024
GITHUB: https://github.com/noesantib1999/ICE_ICE
Purpose: This script directly controls the velocities of each servo for use in controlling ICE catheter manipulation. It is capable of receiving velocity commands over serial interface at 9600 baud.
         The script can be run in an emulation mode to simulate a series of potential velocity commands to each servo.
Implementation: Servos are initially moved to "servo_center_pos" defaulting at 135 degrees and run through a short series of positional commands to ensure proper working condition. 
                Script will then accept serial inputs to control servo VELOCITY via the following format:
                "Axx" will set the Anterior-Posterior (AP) servo to rotate at the float value xx in degrees/sec.
                "Ryy" will set the Left-Right (LR) servo to rotate at the float value xx in degrees/sec.
                Should accept only one input at a time. Any other input formats will be ignored.
Instructions: 
  Setup:   Verify system definitions for servo positional travel limit and center position (*refer to "SERVO_CALIBRATION" to verify these limits).
  General: Ensure that servos are connected to power and their respective pins. Connect the Teensy to a computer establishing a USB connection.

*/



#include <Servo.h>

// Pin definitions:
#define servo_AP_pin 14
#define servo_LR_pin 15

// System definitions:
#define servo_pos_limit 80 // Maximum amount servo should turn in a given direction in degrees, max is 135
#define servo_center_pos 135 // Servo position when catheter is straight

Servo servo_AP;
Servo servo_LR;

bool emulationMode = false; // When true, will not attempt serial connection and will go through some set commands
                            // When false, will connect to serial and receive/plot commands/values
        int loopstate = 0;  // Ignore if not running emulation mode

float cmd_Vel_AP = 0; // Units of degrees per second
float cmd_Vel_LR = 0;

float cmd_Pos_AP = servo_center_pos; // Units of degrees. Set to center_pos so the code starts it here.
float cmd_Pos_LR = servo_center_pos;

unsigned long t0 = micros();
unsigned long t_loop = 0;
unsigned long t_total = 0;
unsigned long t_cycle_0 = 0;

float setServoPos(Servo &servoObj,float cmdPos){
  //cmdPos is in degrees. This needs to be constrained and then remapped to microseconds
  float cmdPos_constrained = constrain(cmdPos,servo_center_pos-servo_pos_limit,servo_center_pos+servo_pos_limit); //Constrains the command degrees to center +- limit
  int cmdPos_micros = map(cmdPos_constrained,0, 270, 500, 2500); // The servo operates between 0 and 270 degrees for 500-2500 microseconds
  servoObj.writeMicroseconds(cmdPos_micros); // Using microseconds instead of regular servo.write() due to servo functionality;
  return cmdPos_constrained; // Rewrite the command position to the constrained position.
}

void handleSerialOutput(float cmd_Vel_AP, float cmd_Pos_AP, float cmd_Vel_LR, float cmd_Pos_LR, float t_loop)
{
  Serial.print("AP_Vel:"); Serial.print(cmd_Vel_AP); Serial.print("\n");
  Serial.print("AP_Pos:"); Serial.print(cmd_Pos_AP); Serial.print("\n");
  Serial.print("LR_Vel:"); Serial.print(cmd_Vel_LR); Serial.print("\n");
  Serial.print("LR_Pos:"); Serial.print(cmd_Pos_LR); Serial.print("\n");
  Serial.print("T_loop:"); Serial.print(t_loop); Serial.print("\n");
  Serial.println("________________________________________");
}

void handleSerialInput(float* cmd_Vel_AP, float* cmd_Vel_LR){
  while ( Serial.available() ){
    int inByte = Serial.read();
    switch (inByte) {
      case 'A':
        *cmd_Vel_AP = Serial.parseFloat();
        Serial.print("AP set to "); Serial.print(*cmd_Vel_AP); Serial.print("\n");
        break;
      case 'R':
        *cmd_Vel_LR = Serial.parseFloat();
        Serial.print("LR set to "); Serial.print(*cmd_Vel_LR); Serial.print("\n");
        break;
      default:
        Serial.println("ERROR: Failed to parse input");

    }
  }
}

void setup() {
  servo_AP.attach(servo_AP_pin,500,2500);
  servo_LR.attach(servo_LR_pin,500,2500);

  if (!emulationMode){
    Serial.begin(9600);
    Serial.println("Serial connected, running simple servo commands...");
    delay(500);
  }

  //Run servos through small commands to ensure hardware is connected and working.
  float temp_Pos_AP; // 
  float temp_Pos_LR;

  temp_Pos_AP = setServoPos(servo_AP, servo_center_pos+10);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_pos+10);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(500);
  temp_Pos_AP = setServoPos(servo_AP, servo_center_pos);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_pos);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(500);
  temp_Pos_AP = setServoPos(servo_AP, servo_center_pos-10);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_pos-10);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(500);
  temp_Pos_AP = setServoPos(servo_AP, servo_center_pos);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_pos);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(500);

  if (!emulationMode){
  Serial.begin(9600);
  Serial.println("Listening to serial input\n");
  Serial.clear();
  delay(500);
  }

}


void loop() {
  t0 = micros();

  if (!emulationMode)
  {
     handleSerialInput(&cmd_Vel_AP, &cmd_Vel_LR); 
  } else {
    t_total = micros()-t_cycle_0;
    if (t_total>=3000000) { // Cycle switches every 3 seconds
      t_cycle_0 = micros();
      loopstate = (loopstate+1)%4; // there are 4 cycle states
      // Serial.println(loopstate);
    }

    switch (loopstate) {
      case 0:
        cmd_Vel_AP = 10;
        cmd_Vel_LR = 10;
        break;
      case 1:
        cmd_Vel_AP = 20;
        cmd_Vel_LR = 20;
        break;
      case 2:
        cmd_Vel_AP = -10;
        cmd_Vel_LR = -10;
        break;
      case 3:
        cmd_Vel_AP = -20;
        cmd_Vel_LR = -20;
        break;
    }
    // low speed for 3 seconds, higher speed for 3 seconds, then switch and do the same in reverse
  }

  delay(10); // Very important - The main loop runs very fast (several us), so this slows it down to a reasonable refresh rate.

  // This block adds a step to the command position dictated by the command velocity
  float cmd_step_AP = cmd_Vel_AP*t_loop/1000000; //dx = dx/dt * dt
  float cmd_step_LR = cmd_Vel_LR*t_loop/1000000;

  cmd_Pos_AP = cmd_Pos_AP+cmd_step_AP;
  cmd_Pos_LR = cmd_Pos_LR+cmd_step_LR;

  cmd_Pos_AP = setServoPos(servo_AP, cmd_Pos_AP); // If the resulting command position fell outside the range, it will be rewritten here. Otherwise it's identical.
  cmd_Pos_LR = setServoPos(servo_LR, cmd_Pos_LR);

  if (!emulationMode) handleSerialOutput(cmd_Vel_AP, cmd_Pos_AP, cmd_Vel_LR, cmd_Pos_LR, t_loop); // Comment this out to not get bombarded with numbers

  t_loop = micros()-t0;
}
