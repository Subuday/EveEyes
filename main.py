import math
import tkinter as tk


class Eye:

    def __init__(
        self,
        width: int,
        height: int,
        center_x: int,
        center_y: int,
        rotation_angle: int,
        num_lines
    ):
        self.width = width
        self.height = height
        self.center_x = center_x
        self.center_y = center_y
        self.rotation_angle = rotation_angle
        assert num_lines % 2 == 0, "Number of lines must be even"
        self.num_lines = num_lines

    def draw(self, canvas: tk.Canvas):
        self._create_oval_polygon(
            canvas,
            self.center_x,
            self.center_y,
            self.width,
            self.height,
            self.rotation_angle,
            self.num_lines
        )

    def _create_oval_polygon(self, canvas, center_x, center_y, width, height, rotation_angle, num_lines):
        # Calculate angle step for the number of segments
        assert num_lines % 2 == 0, "Number of lines must be even"

        steps = num_lines
        step_angel = 2 * math.pi / steps

        rotation_radians = math.radians(-rotation_angle)
    
        # Create a list of points for the oval polygon
        points = []
        oval_points = []
        for i in range(steps):
            # Calculate the angle for this segment
            angle = i * step_angel

            # Calculate the oval points in the oval space
            x = width / 2 * math.cos(angle)
            y = height / 2 * math.sin(angle)

            # Rotate the oval points
            rotated_x = x * math.cos(rotation_radians) - y * math.sin(rotation_radians)
            rotated_y = x * math.sin(rotation_radians) + y * math.cos(rotation_radians)

            points.extend([rotated_x, rotated_y])
            oval_points.extend([center_x + rotated_x, center_y + rotated_y])

        canvas.create_polygon(oval_points, outline='blue', fill='black')

        y_coords = points[1::2]

        theta = math.radians(rotation_angle)
        a = width / 2
        b = height / 2
        for y in sorted(y_coords):
            bd = y * math.sin(2 * theta) * (1/b**2 - 1/a**2)
            ad = math.cos(theta)**2/a**2 + math.sin(theta)**2/b**2
            c = y**2 * (math.sin(theta)**2/a**2 + math.cos(theta)**2/b**2) - 1
            disc = bd**2 - 4 * ad * c
            print(disc)
            if disc < 0:
                continue

            x1 = (-bd - math.sqrt(disc)) / (2 * ad)
            x2 = (-bd + math.sqrt(disc)) / (2 * ad)
            print(f"x1: {x1}, x2: {x2}")

            x1 = center_x + x1
            x2 = center_x + x2
            y = center_y + y

            canvas.create_line(x1, y, x2, y, fill='red')


class Eyes:

    def __init__(
        self,
        spacing: int,
        rotation_angle: int,
        eye_width: int,
        eye_height: int,
        eye_num_lines: int
    ):
        eye_center_y = 172
        eye1_center_x = 194
        self.eye1 = Eye(
            width=eye_width,
            height=eye_height,
            center_x=eye1_center_x,
            center_y=eye_center_y,
            rotation_angle=rotation_angle,
            num_lines=eye_num_lines
        )

        eye2_center_x = eye1_center_x + eye_width / 2 + spacing + eye_width / 2
        self.eye2 = Eye(
            width=eye_width,
            height=eye_height,
            center_x=eye2_center_x,
            center_y=eye_center_y,
            rotation_angle=180 - rotation_angle,
            num_lines=eye_num_lines
        )

    def draw(self, canvas: tk.Canvas):
        self.eye1.draw(canvas)
        self.eye2.draw(canvas)
    

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Eve Eyes')
    root.geometry("680x340")
    root.configure(background='#000000')

    canvas = tk.Canvas(root, width=680, height=340, bg='black')
    canvas.pack()

    eyes = Eyes(
        spacing=92,
        rotation_angle=-16,
        eye_width=188,
        eye_height=124,
        eye_num_lines=100
    )
    eyes.draw(canvas)
    
    root.mainloop()