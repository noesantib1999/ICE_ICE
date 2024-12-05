import tkinter as tk
import math

root = tk.Tk()
root.title("GUI")
root.geometry("640x480")
root.configure(background="white")
root.resizable(False, False)

frame1 = tk.Frame(root, width=150, height=480, bg="gray")
frame1.pack(side=tk.LEFT)

frame2 = tk.Frame(root, width=470, height=480, bg="gray")
frame2.pack(side=tk.RIGHT)

ramp = tk.Spinbox(frame1, from_=1, to=5, width=5)
ramp.place(x=15, y=300)

def update_scrollbar1(value):
    label1.config(text=f"A/P: {value}")

def update_scrollbar2(value):
    label2.config(text=f"R/L: {value}")

def reset_scrollbar1(event):
    scrollbar1.set(0)
    label1.config(text="A/P: 0")

def reset_scrollbar2(event):
    scrollbar2.set(0)
    label2.config(text="R/L: 0")

label1 = tk.Label(frame2, text="A/P: 0", bg="gray", fg="black")
label1.place(x=340, y=15)
label2 = tk.Label(frame2, text="R/L: 0", bg="gray", fg="black")
label2.place(x=410, y=15)

scrollbar1 = tk.Scale(frame2, from_=25, to=-25, orient=tk.VERTICAL, bg="white", width=20,
                      command=update_scrollbar1)
scrollbar1.place(x=330, y=40, height=150)
scrollbar1.bind("<ButtonRelease-1>", reset_scrollbar1)

scrollbar2 = tk.Scale(frame2, from_=25, to=-25, orient=tk.VERTICAL, bg="white", width=20,
                      command=update_scrollbar2)
scrollbar2.place(x=400, y=40, height=150)
scrollbar2.bind("<ButtonRelease-1>", reset_scrollbar2)

current_marker = None
circle_center_x, circle_center_y = 100, 100  # Center of the canvas
circle_radius = 100

def click(event):
    global current_marker 
    x, y = event.x, event.y
    xx = x - circle_center_x
    yy = -(y - circle_center_y)

    # Check if point is outside the circle
    distance = math.sqrt(xx**2 + yy**2)
    if distance > circle_radius:
        # Adjust the x and y values to keep the point inside the circle
        angle = math.atan2(yy, xx)  # Calculate angle to preserve direction
        xx = int(circle_radius * math.cos(angle))
        yy = int(circle_radius * math.sin(angle))
        x = circle_center_x + xx  # Convert back to canvas coordinates
        y = circle_center_y - yy

    if current_marker:
        canvas.delete(current_marker)
    
    radius = 5
    current_marker = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, 
                                        fill="black")
    label7.config(text=f"Coordinates: ({xx}, {yy})")  # Update the label text

def reset_marker():
    global current_marker 
    if current_marker:
        canvas.delete(current_marker)
    radius = 5
    current_marker = canvas.create_oval(circle_center_x - radius, circle_center_y - radius,
                                        circle_center_x + radius, circle_center_y + radius,
                                        fill="black")
    label7.config(text="Coordinates: (0, 0)")  # Reset the label text

button = tk.Button(frame1, text="E-STOP", bg="red", width=15, height=2, command=reset_marker)
button.place(x=15, y=400)

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

# Add label above canvas to display coordinates
label7 = tk.Label(frame2, text="Coordinates: (0, 0)", bg="gray", fg="black")
label7.place(x=90, y=100)

root.mainloop()
