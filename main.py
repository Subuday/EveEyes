import math
from time import sleep
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
        assert num_lines % 2 == 0, "Number of lines must be even"
        self.lines = self._create_lines(width, height, center_x, center_y, rotation_angle, num_lines)

    class State:
        pass

    def _create_lines(self, width, height, center_x, center_y, rotation_angle, num_lines):
        steps = num_lines
        step_angel = 2 * math.pi / steps

        rotation_radians = math.radians(-rotation_angle)
    
        # Create a list of points for the oval polygon
        points = []
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

        y_coords = points[1::2]

        a = width / 2
        b = height / 2
        theta = math.radians(rotation_angle)
        lines = []
        for y in sorted(y_coords):
            bd = y * math.sin(2 * theta) * (1/b**2 - 1/a**2)
            ad = math.cos(theta)**2/a**2 + math.sin(theta)**2/b**2
            c = y**2 * (math.sin(theta)**2/a**2 + math.cos(theta)**2/b**2) - 1
            disc = bd**2 - 4 * ad * c
            if disc < 0:
                continue

            x1 = (-bd - math.sqrt(disc)) / (2 * ad)
            x2 = (-bd + math.sqrt(disc)) / (2 * ad)

            x1 = center_x + x1
            x2 = center_x + x2
            y = center_y + y

            lines.append((x1, y, x2, y))
        
        return lines

    def draw(self, state: State, canvas: tk.Canvas):
        from eye_states import Blinking
        if isinstance(state, Blinking):
            num_lines = len(self.lines)
            num_invisible_lines = int(state.value / 100 * num_lines)
            visible_lines_indices = range(num_invisible_lines // 2, num_lines - num_invisible_lines // 2)

            for i, line in enumerate(self.lines):
                if i in visible_lines_indices:
                    x1, y1, x2, y2 = line
                    canvas.create_line(x1, y1, x2, y2, fill='blue')

blinking_value = 0
blinking_inverted = False

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
        self.canvas = None

    def run(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.blink()

    def blink(self):
        from eye_states import Blinking
        global blinking_value
        global blinking_inverted
        canvas.delete('all')
        state = Blinking(value=blinking_value)
        self.eye1.draw(state, canvas)
        self.eye2.draw(state, canvas)

        if blinking_value == 100:
            blinking_inverted = True
        elif blinking_value == 0:
            blinking_inverted = False

        if not blinking_inverted:
            blinking_value += 10
            canvas.after(50, self.blink)
        else:
            blinking_value -= 10
            canvas.after(50, self.blink)




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
    eyes.run(canvas)
    
    root.mainloop()