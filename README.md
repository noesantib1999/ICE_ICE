# Robotic ICE Catheter
Testing of 2-DOF Robotic ICE Catheter Manipulator for Minimally Invasive, Intracardiac Surgery

## Overview 
### Background
Minimally invasive surgery (MIS) and robot-assisted surgery (RAS) are becoming more commonly used approaches to treat high-risk procedures due to their small-incision operation area, and enhanced precision and control, respectively. By combining these two methods together, you can get increased efficiency and effectiveness in various surgical operations. In cardiology, for example, they allow for reduced mortality rates, lower median length of stay, less blood transfusions, and decreased risks of infection across different studies.

![MIS/RAS](https://stgaccinwbsdevlrs01.blob.core.windows.net/newcorporatewbsite/blogs/october2023/detail-main-Robotic-Heart-Surgery.jpeg)

Among the different areas in cardiology, echocardiography (or cardiac ultrasound) is one where RAS is still being  prototyped. Transesophageal echocardiography (TEE) in particular, a historically common MIS procedure for heart ultrasound through the esophagus, has been the main method used to develop robot-assisted techniques, with outcomes such as reduced radiation exposure, precise, flixible control, and low-latency teleoperations. However, intracardiac echocardiography (ICE) is currently the most adopted method for examining ultrasound due to its thin catheter profile and ability to traverse through the heart chambers. Moreover, compared to TEE, ICE procedures tend to result in shorter length of stay, reduced fluoroscopy and sedation, and closer field of view to desired heart regions. However, this approach is still novel in robotic integration, leaving an opportunity for development of an ICE robotically-assisted system.

![ICE](https://www.stryker.com/content/dam/stryker/endoscopy/products/acunav/images/AcuNav_Silo_Shadow_Left.png)
### Goal
Design, build, and test a 2-DOF robotic mechanism adapter for effective navigation of an intracardiac echocardiography (ICE) catheter through a heart.
## Hardware
### Medical Equipment
- ACUSON Acunav 8F Ultrasound Catheter (for Siemens Systems) 
- ACUSON P500 Ultrasound System

### Electronics
- Teensy 4.0 w/ Micro-USB to USB cable
- 2 Miuzei High-Torque (25 kg*cm) Waterproof Servo Motors w/ cross-shaped servo arm
- Video capture unit (ex. ElGato HD60 X) w/ HDMI and USB connections

### Other Materials
- 3D Printed Parts (PLA filament, 15% infill) - see CAD Designs folder for files
- AC-to-DC Power Supply (4.8-8.4 V Output)
- 2 D-Profile Rotary Shafts (1/2" Diameter, 6" Long, 1045 Carbon Steel) - McMaster number: 8632T134
- 4 Oil-Embedded Bronze Sleeve Bearings (5/8" Housing ID, 5/16" Long, for 1/2" Shaft Diameter) - McMaster number: 6391K736
- Breadboard
- Wires

## Assembly
### CAD Assembly:
The full assembly of the robotic ICE catheter is available when navigating to the CAD Designs folder, and into the "SolidWorks Files - Final" subfolder. Here, the different SLDPRT and SLDASM files that contribute to the complete 3D assembled view in SolidWorks can be located. The CAD Designs folder also has a "STL Files - Final" subfolder, which contains all the STL files needed for 3D printing, along with a short instruction set. You will need slicing software and a 3D printer, such as PrusaSlicer and the Prusa MK3S printer, respectively. Use PrusaSlicer to create a G-code for the STL files, and print each part from the G-code as required. Refer to the specifications in the short instruction set to ensure all parts are properly printed.

### Mechanical Assembly:
After printing, begin assembling the components. The Shaft_Support part is designed to connect two servos, while the ICE_Support_0000 serves to hold the ICE catheter. Position and secure the printed components to hold these parts in place. Ensure proper alignment and fit as per the CAD model.

### Electrical Assembly:
Wire the two Miuzei servos to the Teensy 4.0 as shown in the provided circuit diagram. Ensure all electrical connections are made securely, following the correct wiring paths for power and signal transmission between the components. Verify that all connections are stable and functional before proceeding to the next steps in testing and calibration.

![circuit](https://github.com/user-attachments/assets/4ba8add6-169e-4741-865c-dd9f1d21a488)


## Firmware
Included in this repository are two scripts intended to be run on a Teensy 4.0 (or equivalent board with modifications). These scripts should be uploaded to the Teensy board using a serial USB connection via the Arduino IDE. Each script is also capable of, but does not necessarily require, two-way communication with a computer via this serial USB connection. The functionality and intended use cases of each script are detailed below.

### TEENSY INTERFACE
- Purpose: The TEENSY INTERFACE script directly controls the velocities of each servo for use in controlling ICE catheter manipulation. It is capable of receiving velocity commands over serial interface at 9600 baud. The script can be run in an emulation mode (defined by the variable "emulationMode") to simulate a series of potential velocity commands to each servo. 
- Instructions:
    - Setup:   Verify system definitions for servo positional travel limit and center position (refer to SERVO_CALIBRATION to verify these limits). We recommend using a center position of 135 and travel limit of 80 during typical operating conditions with a 1:1 servo gear ratio. 
    - General: Ensure that servos are connected to power and their respective pins. Connect the Teensy to a computer establishing a USB connection.
    - Use: 
        - Emulation true - The Teensy will not wait for nor respond to instructions though serial communications.
        - Emulation false - Individual servo velocities are controlled by the Teensy as directed by serial communication commands. 
        
### SERVO CALIBRATION
- Purpose: This script directly controls the positions of each servo for use in initial hardware assembly and troubleshooting. Servos are initially moved to "servo_center_pos" defaulting at 135 degrees (recommended). Script will then accept serial inputs to control servo position.
- Instructions: 
    - General:  Ensure that servos are connected to power and their respective pins. Connect the Teensy to a computer establishing a USB connection.
    - Use:      Prior to assembling the ICE hardware, ensure servos positions are set to 135 using this script and can otherwise move freely. Assemble servo gear interface with the ICE catheter in its home position (completely straight). Once assembled, ensure servos can spin by setting the position to a slightly different value using the above format. Progressively test values closer to both 0 and 270 and identify the furthest distance the servos can spin from the home position. Use this to update "servo_pos_limit" for both this script and "TEENSY_INTERFACE."

### Note on firmware commands via serial communication:
Commands must be passed to the Teensy as text strings with a format of either "Ax.x" or "Rx.x" where A and R refer to the antero-posterior and right-left catheter knobs to be controlled and x.x refers to any floating point number. Commands can either be sent through the Arduino IDE in the serial monitor or using the software GUI described below.

## Software
Design the Python Graphical User Interface(GUI) 


## Experimental Setup

### In-Situ Testing 
The experimental setup consisted of having the robotic ICE catheter connected to the ACUSON P500 system to get an ultrasound view of a human heart on the machine. To start, the P500 was connected via HDMI to a video capture unit, gathering the live ultrasound frame and sending it over to the main computer via USB connection. The image from the P500 would then show in the GUI program. 

The TEENSY_INTERFACE.ino code is uploaded into the Teensy 4.0 microcontroller, and remains connected via USB to the main computer. After closing the Arduino IDE program, go to a Python prorgamming software, open GUI_Live.py, and run the GUI. After the GUI is opened, the ultrasound tip of the ICE catheter is inserted into the container with the human heart. From here, the catheter can be oriented through clicking on the coordinate system or the scrollbars in the GUI.

### "Teleoperations" via video conferencing application
One extra step considered for a method of teleoperation was the use of video conferencing software.

## Results


