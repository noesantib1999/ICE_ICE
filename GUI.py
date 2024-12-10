import tkinter as tk
import math
import serial
import threading

# Initialize the serial connection
try:
    ser = serial.Serial('COM8', 9600, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    ser = None

# Function to send data to the serial port
def send_to_serial(data):
    if ser and ser.is_open:
        ser.write(f"{data}\n".encode())

# Function to listen to incoming data on the serial port
def serial_listener():
    while ser and ser.is_open:
        try:
            incoming_data = ser.readline().decode().strip()
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
radio1.place(x=10, y=50)
radio2.place(x=10, y=80)
radio3.place(x=10, y=110)

# Global variables
e_stop_active = False
scrollbar1_target = 0
scrollbar2_target = 0

def update_scrollbar_value(scrollbar, current_value, target_value, step):
    """Gradually update scrollbar value towards the target value."""
    global e_stop_active

    if e_stop_active:
        # Immediately set to zero if E-STOP is active
        scrollbar.set(0)
        return

    if abs(target_value - current_value) <= abs(step):
        scrollbar.set(target_value)
    else:
        new_value = current_value + step
        scrollbar.set(new_value)

        # Use the delay value from the Radiobuttons
        delay = delay_value.get()
        root.after(delay, update_scrollbar_value, scrollbar, new_value, target_value, step)

def click(event):
    global current_marker, e_stop_active, scrollbar1_target, scrollbar2_target
    e_stop_active = False  # Disable E-STOP on user interaction

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

    # Set new targets and initiate gradual update
    scrollbar1_target = xx
    scrollbar2_target = yy
    update_scrollbar_value(scrollbar1, scrollbar1.get(), scrollbar1_target, 1 if xx > scrollbar1.get() else -1)
    update_scrollbar_value(scrollbar2, scrollbar2.get(), scrollbar2_target, 1 if yy > scrollbar2.get() else -1)

    if current_marker:
        canvas.delete(current_marker)

    radius = 5
    current_marker = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")
    label7.config(text=f"Coordinates: ({xx}, {yy})")

def reset_marker():
    """Emergency stop: instantly reset all values to zero."""
    global current_marker, e_stop_active, scrollbar1_target, scrollbar2_target
    e_stop_active = True  # Activate E-STOP

    # Reset targets and scrollbars
    scrollbar1_target = 0
    scrollbar2_target = 0
    scrollbar1.set(0)
    scrollbar2.set(0)
    label1.config(text="R/L: 0")
    label2.config(text="A/P: 0")
    label7.config(text="Coordinates: (0, 0)")

    # Reset canvas marker to the center
    if current_marker:
        canvas.delete(current_marker)
    radius = 5
    current_marker = canvas.create_oval(circle_center_x - radius, circle_center_y - radius,
                                        circle_center_x + radius, circle_center_y + radius,
                                        fill="black")

    # Send stop signal to serial
    send_to_serial("R/L: 0")
    send_to_serial("A/P: 0")

# Labels for scrollbars
label1 = tk.Label(frame2, text="R/L: 0", bg="gray", fg="black")
label1.place(x=340, y=15)

label2 = tk.Label(frame2, text="A/P: 0", bg="gray", fg="black")
label2.place(x=410, y=15)

# Scrollbars for X and Y axes
scrollbar1 = tk.Scale(frame2, from_=100, to=-100, orient=tk.VERTICAL, bg="white", width=20)
scrollbar1.place(x=330, y=40, height=150)

scrollbar2 = tk.Scale(frame2, from_=100, to=-100, orient=tk.VERTICAL, bg="white", width=20)
scrollbar2.place(x=400, y=40, height=150)

# Canvas for drawing
canvas = tk.Canvas(frame2, width=200, height=200, bg="gray", highlightthickness=0)
canvas.place(x=50, y=150)

circle_center_x, circle_center_y = 100, 100
circle_radius = 100
current_marker = None

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

label7 = tk.Label(frame2, text="Coordinates: (0, 0)", bg="gray", fg="black")
label7.place(x=90, y=100)

# Reset button
button = tk.Button(frame1, text="E-STOP", bg="red", width=15, height=2, command=reset_marker)
button.place(x=15, y=400)

root.mainloop()
