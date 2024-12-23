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
- Laptop w/ Python and Arduino/C++ coding software (x2 if using teleoperations)

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

![CAD_Assem](https://github.com/user-attachments/assets/433dc117-a7c4-4965-8ba3-e9c54fd221bf)

### Mechanical Assembly:
After printing, begin assembling the components. The Shaft_Support part is designed to connect two servos, while the ICE_Support_0000 serves to hold the ICE catheter. Position and secure the printed components to hold these parts in place. Ensure proper alignment and fit as per the CAD model.

![Mech](https://github.com/user-attachments/assets/2c52713e-9417-4d96-b5b5-a5ff7f21f95e)

### Electrical Assembly:
Wire the two Miuzei servos to the Teensy 4.0 as shown in the provided circuit diagram. Ensure all electrical connections are made securely, following the correct wiring paths for power and signal transmission between the components. Verify that all connections are stable and functional before proceeding to the next steps in testing and calibration.

![circuit](https://github.com/user-attachments/assets/4ba8add6-169e-4741-865c-dd9f1d21a488)

On the breadboard, the arrangement should be as follows.

![breadboard](https://github.com/user-attachments/assets/6cc4fd08-1e57-42a6-866c-6acfeca9daa7)

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
The objective for this part was to develop a graphical user interface (GUI) to enable intutive control of robot motion via the Teensy microcontroller. Taking this into consideration, the GUI would allow users to input desired velocities for two axes - Left/Right and Posterior/Anterior -, implementing a smooth gradual velocity adjustment to the desired location. Additionally, the GUI would have a coordinate system to click on and automatically guide the catheter through precise motion control.

### Graphical User Interface (GUI)
The purpose of this GUI is to enable users control of the robotic ICE catheter via serial connection. For starters, open GUI_Live.py and make sure that the microcontroller's serial USB connection is the same as the "port" value in line 11 of the code; if not, update it. Once updated, run the code in a Python programming software to open the GUI.

The GUI contains the following items:
- E-STOP button: located in the top left part of the screen in a bright red color, it serves as an override button and instantly changes the robotic ICE catheter's velocity vector to zero.
- Velocity update rate: placed below the E-STOP button to the left. With these three buttons, choose the velocity delay value, with the default value set as 10 (smallest is fastest).
- Instantaneous velocity scrollbars: with this input method, change the angular velocity rate instantly by moving the scrollbars, each labeled with their respective movement axis.
- Coordinate system: located below the button and scrollbars. Click on the coordinate system to change the velocity vector, moving the catheter at the desired rate.
- Live Ultrasound Feedback: located on the right side of the screen; a live image of the ultrasound can be displayed using VideoCapture() and through effective connection from the ultrasound viewing system to the main computer using a video capture unit.

![GUI](https://github.com/user-attachments/assets/19fe92f3-274b-487e-b126-9bffe3123fa1)

### Teleoperations via UDP/Sockets

Two additional codes are also included in the Software folder, named Tele_GUI_Send.py and Tele_ICE_Receive.py, used for teleoperations with sockets and UDP packets. For this approach, use one computer as the "sender", which will run the Tele_GUI_Send.py code and utilize the GUI the same way as before to send the velocity vectors as UDP packets to the "receiver", another computer which runs the Tele_ICE_Receiver.py code and connects to the Teensy microcontroller via serial connection.
- Note: make sure both sets of code have the same gateway port number to ensure effective connection between the computers. Additionally, search for the receiver's IP address via "ipconfig" in your command window, and copy/paste the IPv4 address into the Tele_GUI_Send.py script in line 8.

## Experimental Setup

### In-Situ Testing 
![InSitu](https://github.com/user-attachments/assets/8e0514d9-d63b-4417-b1f8-58abdafe40af)

The experimental setup consisted of having the robotic ICE catheter connected to the ACUSON P500 system to get an ultrasound view of a human heart on the machine. To start, the P500 was connected via HDMI to a video capture unit, gathering the live ultrasound frame and sending it over to the main computer via USB connection. The image from the P500 would then show in the GUI program. 

- Note: The procedure can be replicated if the ICE catheter and ultrasound viewing system are compatible (both are from the same brand). Additionally, check whether the HDMI ports in the ultrasound system are IN or OUT, as video capture units tend to receive the image from OUT ports.

The TEENSY_INTERFACE.ino code is uploaded into the Teensy 4.0 microcontroller, and remains connected via USB to the main computer. After closing the Arduino IDE program, go to a Python prorgamming software, open GUI_Live.py, and run the GUI. After the GUI is opened, the ultrasound tip of the ICE catheter is inserted into the container with the human heart. From here, the catheter can be oriented through clicking on the coordinate system or the scrollbars in the GUI.

Movement of the catheter through the heart for this experiment is straightforward: the catheter will enter through the inferior vena cava (IVC) and examine the right atrium. Some movements with the GUI would be performed before moving forward to the right ventricle, where the experiment concludes.

### "Teleoperations" via video conferencing application
One extra step considered for a method of teleoperation is the use of video conferencing software. By having two computers access the same conference link, the main computer (connected to the Teensy 4.0) can grant desktop control to the external computer and the latter can guide the ICE catheter through the GUI program. 

![VC_Tele](https://github.com/user-attachments/assets/8a37e7d6-7cf4-4bc2-9a2e-971435b32b6e)

### UDP/Sockets Teleoperations
Using Tele_GUI_Send.py and Tele_ICE_Receive.py, the "sender" computer would run the GUI program, operate the controls, and send the infomation via UPD packets to the "receiver" computer, operating the robotic ICE catheter.

## Results
### In-Situ

The experiments were attempted on two different human hearts from the Visible Heart Lab's Heart Library. For Heart #1, placed in a small container with water, the catheter entered through the IVC and was able to reach the right atrium. However, after moving the catheter using the coordinate system of the GUI, the velocity vectors were be very high and prevented movement into the right ventricle. After using the scrollbars to manually control the servos and guide it to the right ventricle.

![InSitu_Test](https://github.com/user-attachments/assets/66576977-16b4-4cbb-95d9-17b3c74b1b70)

For Heart #2, the experiment was done in a wider container, which caused the heart to have less constrained movement and follow the displacement of the ICE catheter, affecting the ultrasound image result. After grabbing ahold of the heart, the movement of the ICE catheter performed similar to Heart #1.

Some considerations to add after this initial experimental setup is to set the heart in a static position in the container to have effective movement of the ultrasound tip through the heart chambers. Additionally, it is recommended that the velocity vectors are reduced to prevent any quick changes in movement inside the heart and affecting the patient, as well as having a position-based system for more effective ICE catheter orientation.

### "Teleoperations"

This approach was only tested in Heart #1. From the external computer, evident lag and low resoulution quality were found, making it challenging to move the scrollbars and observe the desired heart regions via the ultrasound. Although an effective proof of concept, it is recommended to consider other approaches. 

![Zoom_tele](https://github.com/user-attachments/assets/2fa2cbcf-683b-4f2e-87aa-588779824f61)

### Teleoperations

Due to time constraints, this approach was not yet tested in a human heart. However, teleoperation results showed low-latency communications between the two computers, making it an effective method for sending data over the internet to operate the robotic ICE catheter. One observation from these tests, nonetheless, is that when utilizing the scrollbars for changing the velocity vectors, the Tele_ICE_Receiver.py code waited for the main "sender" computer to stop sending data to ultimately perform the movement. Further examination is required to verify whether this approach is helpful or can place challenges when needing to send multiple data packets in a short time period.

![Tele_Test](https://github.com/user-attachments/assets/af1b8d5c-1c87-46f9-8ad6-44e84cc3f9f3)

## Credits
ME 8284 - Intermediate Robotics with Medical Applications (Graduate-Level Course)

Team Prince: <br>
Team Manager - Noé Bazán (baznp001@umn.edu) <br>
Mechanical Leads - Anders Torp (gloeg011@umn.edu) and Rucha Pansare (pansa008@umn.edu)<br>
Embedded Lead - Michael Feldkamp (feldk066@umn.edu)<br>
Software Lead - Shrivatsa Deshmukh (deshm080@umn.edu)<br>
Floater - Tianning Li (li003291@umn.edu)

Presentation Link (from December 10th 2024): https://docs.google.com/presentation/d/189g-k64IC7r7hnKr-tXK-r5zNP0DUaRn04MexWa3yLw/edit?usp=sharing
