import tkinter as tk
import math
import socket
import cv2
from PIL import Image, ImageTk

# Configure the gateway’s IP and port
GATEWAY_IP = "10.130.11.86"  # Replace with actual IP of the gateway laptop
GATEWAY_PORT = 8284

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_udp_command(command):
    """Send a command line via UDP to the gateway."""
    sock.sendto(command.encode('utf-8'), (GATEWAY_IP, GATEWAY_PORT))

root = tk.Tk()
root.title("Robotic ICE Prototype Interface")
root.geometry("1530x720")
root.configure(background="white")
root.resizable(False, False)

video_label = tk.Label(root)
video_label.pack()
video_label.place(x=250, y=0)

# Attempt to open the capture device.
# Try changing 0 to 1, 2, etc. if you have multiple cameras.
capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # On Windows, CAP_DSHOW can help.
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
#capture.set(cv2.CAP_PROP_FPS, 60)

def update_frame():
    # Grab a frame from the capture device
    ret, frame = capture.read()
    if not ret:
        # If frame not received, just try again after 10 ms
        root.after(5, update_frame)
        return

    # Convert the frame from BGR (OpenCV format) to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the image to PIL format
    img_pil = Image.fromarray(frame_rgb)

    # Convert PIL image to ImageTk format
    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Update the label with the new image
    video_label.img_tk = img_tk
    video_label.configure(image=img_tk)

    # Schedule the next frame update
    root.after(5, update_frame)

# Frames for layout
frame1 = tk.Frame(root, width=250, height=720, bg="gray")
frame1.pack(side=tk.LEFT)

# Delay control variable
delay_value = tk.IntVar(value=10)

# Radio buttons to select the delay
radio1 = tk.Radiobutton(frame1, text="Delay: 10", variable=delay_value, value=10, bg="gray")
radio2 = tk.Radiobutton(frame1, text="Delay: 50", variable=delay_value, value=50, bg="gray")
radio3 = tk.Radiobutton(frame1, text="Delay: 100", variable=delay_value, value=100, bg="gray")
radio1.place(x=5, y=155)
radio2.place(x=5, y=185)
radio3.place(x=5, y=215)

# Global variables
e_stop_active = False
scrollbar1_target = 0
scrollbar2_target = 0
circle_center_x, circle_center_y = 100, 100
circle_radius = 100
current_marker = None

# Labels for the scrollbars
label1 = tk.Label(frame1, text="R/L: 0", bg="gray", fg="black")
label1.place(x=117, y=100)
label2 = tk.Label(frame1, text="A/P: 0", bg="gray", fg="black")
label2.place(x=187, y=100)
label7 = tk.Label(frame1, text="Coordinates: (0, 0)", bg="gray", fg="black")
label7.place(x=75, y=290)

def update_labels():
    """Update labels and send current values to the serial port."""
    x_val = scrollbar1.get()
    y_val = scrollbar2.get()
    label1.config(text=f"R/L: {x_val}")
    label2.config(text=f"A/P: {y_val}")
    label7.config(text=f"Coordinates: ({x_val}, {y_val})")
    root.update_idletasks()

    # Send updated values via UDP
    send_udp_command(f"R/L: {x_val}")
    send_udp_command(f"A/P: {y_val}")

def update_scrollbar_value(scrollbar, current_value, target_value, step):
    """Gradually update scrollbar value towards the target value."""
    global e_stop_active

    if e_stop_active:
        scrollbar.set(0)
        update_labels()
        return
    # Check if we are close to the target
    if abs(target_value - current_value) <= abs(step):
        # Set final value
        scrollbar.set(target_value)
    else:
        # Move one step towards target
        new_value = current_value + step
        scrollbar.set(new_value)
        # Schedule next update after the chosen delay
        delay = delay_value.get()
        root.after(delay, update_scrollbar_value, scrollbar, new_value, target_value, step)

    # After updating the scrollbar (final or intermediate), update labels
    update_labels()

def click(event):
    """Handle mouse click on the canvas to set new scrollbar targets."""
    global current_marker, e_stop_active, scrollbar1_target, scrollbar2_target
    e_stop_active = False # Disable E-STOP on user interaction

    x, y = event.x, event.y
    xx = x - circle_center_x
    yy = -(y - circle_center_y)

    # Adjust if out of circle range
    distance = math.sqrt(xx**2 + yy**2)
    if distance > circle_radius:
        angle = math.atan2(yy, xx)
        xx = int(circle_radius * math.cos(angle))
        yy = int(circle_radius * math.sin(angle))
        x = circle_center_x + xx
        y = circle_center_y - yy


    # Update targets
    scrollbar1_target = xx
    scrollbar2_target = yy


    update_scrollbar_value(scrollbar1, scrollbar1.get(), scrollbar1_target,
                           1 if xx > scrollbar1.get() else -1)
    update_scrollbar_value(scrollbar2, scrollbar2.get(), scrollbar2_target,
                           1 if yy > scrollbar2.get() else -1)

    if current_marker:
        canvas.delete(current_marker)
    radius = 5
    current_marker = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black")

def reset_marker():
    global current_marker, e_stop_active, scrollbar1_target, scrollbar2_target
    e_stop_active = True
    scrollbar1_target = 0
    scrollbar2_target = 0
    scrollbar1.set(0)
    scrollbar2.set(0)
    update_labels()
    if current_marker:
        canvas.delete(current_marker)
    radius = 5
    current_marker = canvas.create_oval(circle_center_x - radius, circle_center_y - radius,
                                        circle_center_x + radius, circle_center_y + radius,
                                        fill="black")

canvas = tk.Canvas(frame1, width=200, height=200, bg="gray", highlightthickness=0)
canvas.place(x=25, y=340)
canvas.create_oval(circle_center_x - circle_radius, circle_center_y - circle_radius,
                   circle_center_x + circle_radius, circle_center_y + circle_radius,
                   fill="white")
canvas.create_line(circle_center_x - circle_radius, circle_center_y,
                   circle_center_x + circle_radius, circle_center_y,
                   fill="black", width=2)
canvas.create_line(circle_center_x, circle_center_y - circle_radius,
                   circle_center_x, circle_center_y + circle_radius,
                   fill="black", width=2)

label3 = tk.Label(frame1, text="A", bg="gray", fg="black")
label3.place(x=119, y=315)
label4 = tk.Label(frame1, text="P", bg="gray", fg="black")
label4.place(x=119, y=545)
label5 = tk.Label(frame1, text="L", bg="gray", fg="black")
label5.place(x=8, y=428)
label6 = tk.Label(frame1, text="R", bg="gray", fg="black")
label6.place(x=232, y=428)

canvas.bind("<Button-1>", click)

scrollbar1 = tk.Scale(frame1, from_=100, to=-100, orient=tk.VERTICAL, bg="white", width=20,
                      command=lambda val: update_labels())
scrollbar1.place(x=110, y=125, height=150)

scrollbar2 = tk.Scale(frame1, from_=100, to=-100, orient=tk.VERTICAL, bg="white", width=20,
                      command=lambda val: update_labels())
scrollbar2.place(x=180, y=125, height=150)

e_stop_button = tk.Button(frame1, text="E-STOP", bg="red", width=30, height=4, command=reset_marker)
e_stop_button.place(x=15, y=15)

update_frame()
update_labels()
root.mainloop()

capture.release()
cv2.destroyAllWindows()