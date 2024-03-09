import math
import tkinter as tk

def create_oval_polygon(canvas, center_x, center_y, width, height, rotation_angle, num_segments=1000):
    # Calculate angle step for the number of segments
    angle_step = 2 * math.pi / num_segments
  
    # Create a list of points for the oval polygon
    points = []
    for i in range(num_segments):
        # Calculate the angle for this segment
        angle = i * angle_step
      
        # Calculate the unrotated oval point
        x = center_x + width / 2 * math.cos(angle)
        y = center_y + height / 2 * math.sin(angle)
      
        # Rotate the point
        rotated_x = (x - center_x) * math.cos(math.radians(rotation_angle)) - \
                    (y - center_y) * math.sin(math.radians(rotation_angle)) + center_x
        rotated_y = (x - center_x) * math.sin(math.radians(rotation_angle)) + \
                    (y - center_y) * math.cos(math.radians(rotation_angle)) + center_y
        points.extend([rotated_x, rotated_y])

    # Draw the polygon on the canvas
    canvas.create_polygon(points, fill='blue')

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Eve Eyes')
    root.geometry("680x340")
    root.configure(background='#000000')

    canvas = tk.Canvas(root, width=680, height=340, bg='black')
    canvas.pack()

    eye_width = 188
    eye_height = 124
    eyes_spacing = 92
    eye_center_y = 172

    eye1_center_x = 194
    eye1_rotation_angle = 16
    create_oval_polygon(canvas, eye1_center_x, eye_center_y, eye_width, eye_height, eye1_rotation_angle)

    eye2_center_x = eye1_center_x + eye_width / 2 + eyes_spacing + eye_width / 2
    eye2_rotation_angle = 180 - eye1_rotation_angle
    create_oval_polygon(canvas, eye2_center_x, eye_center_y, eye_width, eye_height, eye2_rotation_angle)
  
    root.mainloop()