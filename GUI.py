import tkinter as tk
import math
import serial
import threading
import time

# Initialize the serial connection

try:
    ser = serial.Serial('COM8', 9600, timeout=1)  
except Exception as e:
    print(f"Error opening serial port: {e}")
    ser = None

# Function to send data to the serial port
def send_to_serial(data):
    if ser and ser.is_open:
        ser.write(f"{data}\n".encode())  # Send data as a string, ending with a newline

# Function to listen to incoming data on the serial port
def serial_listener():
    while ser and ser.is_open:
        try:
            incoming_data = ser.readline().decode().strip()  # Read a line of data
            if incoming_data:
                print(f"Received from serial: {incoming_data}")
        except Exception as e:
            print(f"Error reading from serial: {e}")

# Start the serial listener thread
listener_thread = threading.Thread(target=serial_listener, daemon=True)
listener_thread.start()

# Initialize the root window
root = tk.Tk()
root.title("GUI")
root.geometry("640x480")
root.configure(background="white")
root.resizable(False, False)

# Frames for layout
frame1 = tk.Frame(root, width=150, height=480, bg="gray")
frame1.pack(side=tk.LEFT)

frame2 = tk.Frame(root, width=470, height=480, bg="gray")
frame2.pack(side=tk.RIGHT)

# Variable to control the delay value in root.after()
delay_value = tk.IntVar(value=10)  # Default delay is 10

# Add Radiobuttons to frame1 for controlling the delay
radio1 = tk.Radiobutton(frame1, text="Delay: 1", variable=delay_value, value=1, bg="gray")
radio2 = tk.Radiobutton(frame1, text="Delay: 10", variable=delay_value, value=10, bg="gray")
radio3 = tk.Radiobutton(frame1, text="Delay: 100", variable=delay_value, value=100, bg="gray")

# Pack Radiobuttons
radio1.place(x=10, y=50)
radio2.place(x=10, y=80)
radio3.place(x=10, y=110)

# Scrollbar update functions
def update_scrollbar1(value):
    label1.config(text=f"R/L: {value}")
    send_to_serial(f"R/L: {value}")  # Send the A/P value to the serial port

def update_scrollbar2(value):
    label2.config(text=f"A/P: {value}")
    send_to_serial(f"A/P: {value}")  # Send the R/L value to the serial port

# Store the last clicked coordinates
last_xx, last_yy = 0, 0

def reset_scrollbar1(event):
    scrollbar1.set(last_xx)
    label1.config(text=f"R/L: {last_xx}")

def reset_scrollbar2(event):
    scrollbar2.set(last_yy)
    label2.config(text=f"A/P: {last_yy}")

# Labels for scrollbars
label1 = tk.Label(frame2, text="R/L: 0", bg="gray", fg="black")
label1.place(x=340, y=15)
label2 = tk.Label(frame2, text="A/P: 0", bg="gray", fg="black")
label2.place(x=410, y=15)

# Scrollbars for X and Y axes
scrollbar1 = tk.Scale(frame2, from_=100, to=-100, orient=tk.VERTICAL, bg="white", width=20, command=update_scrollbar1)
scrollbar1.place(x=330, y=40, height=150)
scrollbar1.bind("<ButtonRelease-1>", reset_scrollbar1)

scrollbar2 = tk.Scale(frame2, from_=100, to=-100, orient=tk.VERTICAL, bg="white", width=20, command=update_scrollbar2)
scrollbar2.place(x=400, y=40, height=150)
scrollbar2.bind("<ButtonRelease-1>", reset_scrollbar2)

# Rest of your code remains the same...


# Canvas interaction functions
current_marker = None
circle_center_x, circle_center_y = 100, 100  # Center of the canvas
circle_radius = 100

def update_scrollbar_value(scrollbar, current_value, target_value, step):
    """Smoothly update scrollbar value towards the target value."""
    if abs(target_value - current_value) <= abs(step):
        scrollbar.set(target_value)
    else:
        new_value = current_value + step
        scrollbar.set(new_value)
        
        # Use the delay value from the Radiobuttons for root.after()
        delay = delay_value.get()  
        root.after(delay, update_scrollbar_value, scrollbar, new_value, target_value, step)

def click(event):
    global current_marker, last_xx, last_yy
    x, y = event.x, event.y
    xx = x - circle_center_x
    yy = -(y - circle_center_y)

    distance = math.sqrt(xx**2 + yy**2)
    if distance > circle_radius:
        angle = math.atan2(yy, xx)
        xx = int(circle_radius * math.cos(angle))
        yy = int(circle_radius * math.sin(angle))
        x = circle_center_x + xx
        y = circle_center_y - yy

    # Update scrollbar values smoothly
    step = 1 if xx > last_xx else -1
    update_scrollbar_value(scrollbar1, last_xx, xx, step)
    step = 1 if yy > last_yy else -1
    update_scrollbar_value(scrollbar2, last_yy, yy, step)

    last_xx, last_yy = xx, yy

    if current_marker:
        canvas.delete(current_marker)
    
    radius = 5
    current_marker = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")
    label7.config(text=f"Coordinates: ({xx}, {yy})")

def reset_marker():
    global current_marker, last_xx, last_yy
    scrollbar1.set(0)
    scrollbar2.set(0)
    last_xx, last_yy = 0, 0
    label1.config(text="R/L: 0")
    label2.config(text="A/P: 0")
    label7.config(text="Coordinates: (0, 0)")

    if current_marker:
        canvas.delete(current_marker)
    radius = 5
    current_marker = canvas.create_oval(circle_center_x - radius, circle_center_y - radius,
                                        circle_center_x + radius, circle_center_y + radius,
                                        fill="black")

# Reset button
button = tk.Button(frame1, text="E-STOP", bg="red", width=15, height=2, command=reset_marker)
button.place(x=15, y=400)

# Canvas for drawing
canvas = tk.Canvas(frame2, width=200, height=200, bg="gray", highlightthickness=0)
canvas.place(x=50, y=150)

canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                   circle_center_x + circle_radius, circle_center_y + circle_radius,
                   fill="white")
canvas.bind("<Button-1>", click)

canvas.create_line(circle_center_x - circle_radius, circle_center_y, 
                   circle_center_x + circle_radius, circle_center_y, 
                   fill="black", width=2)
canvas.create_line(circle_center_x, circle_center_y - circle_radius, 
                   circle_center_x, circle_center_y + circle_radius, 
                   fill="black", width=2)

label3 = tk.Label(frame2, text="A", bg="gray", fg="black")
label3.place(x=145, y=125)
label4 = tk.Label(frame2, text="P", bg="gray", fg="black")
label4.place(x=145, y=350)
label5 = tk.Label(frame2, text="L", bg="gray", fg="black")
label5.place(x=35, y=237)
label6 = tk.Label(frame2, text="R", bg="gray", fg="black")
label6.place(x=255, y=237)

# Label above canvas for coordinates
label7 = tk.Label(frame2, text="Coordinates: (0, 0)", bg="gray", fg="black")
label7.place(x=90, y=100)

root.mainloop()
