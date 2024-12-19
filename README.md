# Robotic ICE Catheter
Testing of 2-DOF Robotic ICE Catheter Manipulator for Minimally Invasive, Intracardiac Surgery

## Overview 
### Background
Minimally invasive surgery (MIS) and robot-assisted surgery (RAS) are becoming more commonly used approaches to treat high-risk procedures due to their small-incision operation area, and enhanced precision and control, respectively. By combining these two methods together, you can get increased efficiency and effectiveness in various surgical operations. In cardiology, for example, they allow for reduced mortality rates, lower median length of stay, less blood transfusions, and decreased risks of infection across different studies. Among the different areas in cardiology, echocardiography (or cardiac ultrasound) is one where RAS is still being  prototyped. 

Transesophageal echocardiography (TEE) in particular, a historically common MIS procedure for heart ultrasound through the esophagus, has been the main method used to develop robot-assisted techniques, with outcomes such as reduced radiation exposure, precise, flixible control, and low-latency teleoperations. However, intracardiac echocardiography (ICE) is currently the most adopted method for examining ultrasound due to its thin catheter profile and ability to traverse through the heart chambers. Moreover, compared to TEE, ICE procedures tend to result in shorter length of stay, reduced fluoroscopy and sedation, and closer field of view to desired heart regions. However, this approach is still novel in robotic integration, leaving an opportunity for development of an ICE robotically-assisted system.

### Goal
Design, build, and test a 2-DOF robotic mechanism adapter for navigation of an intracardiac
echocardiography (ICE) catheter through a heart
## Hardware
### Medical Equipment
- ACUSON Acunav 8F Ultrasound Catheter (for Siemens Systems) 
- ACUSON P500 Ultrasound System

### Materials
- 3D Printed Parts (PLA, 15% infill) - see CAD Designs folder for files
- Teensy 4.0 w/ Micro-USB to USB cable
- 2 Miuzei High-Torque (25 kg*cm) Waterproof Servo Motors w/
- AC-to-DC Power Supply (~5.9 V)
- 2 D-Profile Rotary Shafts (1/2" Diameter, 6" Long, 1045 Carbon Steel) - McMaster number: 8632T134
- 4 Oil-Embedded Bronze Sleeve Bearings (5/8" Housing ID, 5/16" Long, for 1/2" Shaft Diameter) - McMaster number: 6391K736
- Breadboard
- Wires

## Assembly
### CAD Assembly:
You can navigate to the CAD Designs folder, and open the folder containing the printed components for the assembly. The folder consists of STL files, which can be viewed in SOLIDWORKS for 3D visualization. Download all the folder contents and ensure all STL files are accounted for. You will need slicing software and a 3D printer. It is recommended to use PrusaSlicer and a Prusa MK3S printer. Use PrusaSlicer to create a G-code for each STL file. Print each part from the G-code as required. Refer to the specifications in the accompanying PDF to ensure all parts meet the design requirements. The SLDASM files will guide you in assembling and ensuring proper alignment of the components.

### Mechanical Assembly:
After printing, begin assembling the components. The printed parts are designed to connect two servos, a Teensy 4.0 microcontroller, and an ICE catheter. Position and secure the printed components to hold these parts in place. Ensure proper alignment and fit as per the CAD model.

### Electrical Assembly:
Wire the two Miuzei servos to the Teensy 4.0 as shown in the provided circuit diagram. Ensure all electrical connections are made securely, following the correct wiring paths for power and signal transmission between the components. Verify that all connections are stable and functional before proceeding to the next steps in testing and calibration.

![image](https://github.com/user-attachments/assets/4ba8add6-169e-4741-865c-dd9f1d21a488)


## Firmware
Two Miuzei servos 25 kg 270°, a teensy 4.0, an ice catheter, a DRV8833 H-Bridge for driving up to two DC motors

## Software
Design the Python Graphical User Interface(GUI) 
