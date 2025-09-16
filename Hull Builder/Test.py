import tkinter as tk

def update_canvas(value):
    canvas.delete("all")  # Clear previous drawing
    x = int(value)
    y = 100
    radius = 50
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="blue")

root = tk.Tk()
root.title("Canvas and Slider Example")

# Create a Canvas
canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.pack()

# Create a Slider (Scale)
slider = tk.Scale(root, from_=50, to=350, orient=tk.HORIZONTAL, label="X Position", command=update_canvas)
slider.pack()

# Initial drawing on the canvas
update_canvas(200)

root.mainloop()