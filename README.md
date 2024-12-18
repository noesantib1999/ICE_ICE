# Robotic ICE Catheter
Testing of 2-DOF Robotic ICE Catheter Manipulator for Minimally Invasive, Intracardiac Surgery

## Overview 
Minimally invasive surgery (MIS) and robot-assisted surgery (RAS) are becoming more commonly used approaches to treat high-risk procedures due to their small-incision operation area, and enhanced precision and control, respectively. By combining these two methods together, you can get increased efficiency and effectiveness in various surgical operations. In cardiology, for example, they allowed for reduced mortality rates, lower median length of stay, less blood transfusions, and smaller risks of infection across different studies. 

### Goal
Design, build, and test a 2-DOF robotic mechanism adapter for navigation of an intracardiac
echocardiography (ICE) catheter through a porcine heart via teleoperation and pedal movement
### Software
Design the Python Graphical User Interface(GUI) 
### Hardware
### Assembly
CAD Assembly:
You can navigate to the CAD Designs folder, and open the folder containing the printed components for the assembly. The folder consists of STL files, which can be viewed in SOLIDWORKS for 3D visualization. Download all the folder contents and ensure all STL files are accounted for. You will need slicing software and a 3D printer. It is recommended to use PrusaSlicer and a Prusa MK3S printer. Use PrusaSlicer to create a G-code for each STL file. Print each part from the G-code as required. Refer to the specifications in the accompanying PDF to ensure all parts meet the design requirements. The SLDASM files will guide you in assembling and ensuring proper alignment of the components.

Mechanical Assembly:
After printing, begin assembling the components. The printed parts are designed to connect two servos, a Teensy 4.0 microcontroller, and an ice catheter. Position and secure the printed components to hold these parts in place. Ensure proper alignment and fit as per the CAD model.

Electrical Assembly:
Wire the two Miuzei servos, Teensy 4.0, and an HW-627 motor controller according to the provided circuit diagram. Ensure all electrical connections are made securely, following the correct wiring paths for power and signal transmission between the components. Verify that all connections are stable and functional before proceeding to the next steps in testing and calibration.


### Firmware
Two Miuzei servos 25 kg 270°, a teensy 4.0, an ice catheter, a DRV8833 H-Bridge for driving up to two DC motors
