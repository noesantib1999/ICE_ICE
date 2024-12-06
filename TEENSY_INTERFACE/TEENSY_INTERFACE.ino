#include <Servo.h>

// Pin definitions:
#define servo_AP_pin 13
#define servo_LR_pin 14

// System definitions:
#define servo_pos_limit 135 // Maximum amount servo should turn in a given direction in degrees, max is 135
#define servo_center_val 135 // Servo position when catheter is straight

Servo servo_AP;
Servo servo_LR;

bool emulationMode = false; // When true, will not attempt serial connection and will go through some set commands
                            // When false, will connect to serial and receive/plot commands/values
        int loopstate = 0;  // Ignore if not running emulation mode

float cmd_Vel_AP = 0; // Units of degrees per second
float cmd_Vel_LR = 0;

float cmd_Pos_AP = 0; // Units of degrees
float cmd_Pos_LR = 0;

unsigned long t0 = micros();
unsigned long t_loop = 0;
unsigned long t_total = 0;

float setServoPos(Servo &servoObj,float cmdPos){
  //cmdPos is in degrees. This needs to be constrained and then remapped to microseconds
  float cmdPos_constrained = constrain(cmdPos,servo_center_val-servo_pos_limit,servo_center_val+servo_pos_limit); //Constrains the command degrees to center +- limit
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
  servo_AP.attach(servo_AP_pin);
  servo_LR.attach(servo_LR_pin);

  if (!emulationMode){
    Serial.begin(9600);
    Serial.println("Serial connected, running simple servo commands...");
    delay(500);
  }

  //Run servos through small commands
  float temp_Pos_AP; // 
  float temp_Pos_LR;

  temp_Pos_AP = setServoPos(servo_AP, servo_center_val+10);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_val+10);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(2000);
  temp_Pos_AP = setServoPos(servo_AP, servo_center_val);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_val);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(2000);
  temp_Pos_AP = setServoPos(servo_AP, servo_center_val-10);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_val-10);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(2000);
  temp_Pos_AP = setServoPos(servo_AP, servo_center_val);
  temp_Pos_LR = setServoPos(servo_LR, servo_center_val);
  //  if (!emulationMode) handleSerialOutput(0, temp_Pos_AP, 0, temp_Pos_LR, 0);
  delay(2000);

  if (!emulationMode){
  Serial.begin(9600);
  Serial.println("Listening to serial input\n");
  Serial.clear();
  }

}


void loop() {
  t0 = micros();

  if (!emulationMode)
  {
     handleSerialInput(&cmd_Vel_AP, &cmd_Vel_LR); 
  } else {
    t_total += micros();
    if (t_total>=3000000) { // Cycle switches every 3 seconds
      t_total = t_total%3000000; 
      loopstate = (loopstate+1)%4; // there are 4 cycle states
    }

    switch (loopstate) {
      case 0:
        cmd_Vel_AP = 2.5;
        cmd_Vel_LR = 2.5;
        break;
      case 1:
        cmd_Vel_AP = 10;
        cmd_Vel_LR = 10;
        break;
      case 2:
        cmd_Vel_AP = -2.5;
        cmd_Vel_LR = -2.5;
        break;
      case 3:
        cmd_Vel_AP = -10;
        cmd_Vel_LR = -10;
        break;
    }
    // 2.5 for 3 seconds, 10 for 3 seconds, then switch and do the same in reverse
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
