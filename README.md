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
- AC-to-DC Power Supply (~5.9 V)
- 2 D-Profile Rotary Shafts (1/2" Diameter, 6" Long, 1045 Carbon Steel) - McMaster number: 8632T134
- 4 Oil-Embedded Bronze Sleeve Bearings (5/8" Housing ID, 5/16" Long, for 1/2" Shaft Diameter) - McMaster number: 6391K736
- Breadboard
- Wires

## Assembly
### CAD Assembly:
The full assembly of the robotic ICE catheter is available when navigating to the CAD Designs folder, and into the "SolidWorks Files - Final" subfolder. Here, the different SLDPRT and SLDASM files that contribute to the complete 3D assembled view in SolidWorks can be located. The CAD Designs folder also has a "STL Files - Final" subfolder, which contains all the STL files needed for 3D printing, along with a short instruction set. You will need slicing software and a 3D printer, such as PrusaSlicer and the Prusa MK3S printer, respectively. Use PrusaSlicer to create a G-code for the STL files, and print each part from the G-code as required. Refer to the specifications in the short instruction set to ensure all parts are properly printed.

### Mechanical Assembly:
After printing, begin assembling the components. The printed parts are designed to connect two servos, the Teensy 4.0 microcontroller, and the ICE catheter. Position and secure the printed components to hold these parts in place. Ensure proper alignment and fit as per the CAD model.

### Electrical Assembly:
Wire the two Miuzei servos to the Teensy 4.0 as shown in the provided circuit diagram. Ensure all electrical connections are made securely, following the correct wiring paths for power and signal transmission between the components. Verify that all connections are stable and functional before proceeding to the next steps in testing and calibration.

![circuit](https://github.com/user-attachments/assets/4ba8add6-169e-4741-865c-dd9f1d21a488)


## Firmware
Two Miuzei servos 25 kg 270°, a teensy 4.0, an ice catheter, a DRV8833 H-Bridge for driving up to two DC motors

## Software
Design the Python Graphical User Interface(GUI) 
