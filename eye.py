import math
from eyes_canvas import EyesCanvas


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
        self.line_color = 'blue'
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
    
    def _draw_default_state(self, canvas: EyesCanvas):
        for x1, y1, x2, y2 in self.lines:
            canvas.create_line(x1, y1, x2, y2, fill=self.line_color)

    def _draw_blinking_state(self, canvas: EyesCanvas, percentage: int):
        num_lines = len(self.lines)
        num_invisible_lines = int(percentage / 100 * num_lines)
        visible_lines_indices = range(num_invisible_lines // 2, num_lines - num_invisible_lines // 2)

        for i, line in enumerate(self.lines):
            if i in visible_lines_indices:
                x1, y1, x2, y2 = line
                canvas.create_line(x1, y1, x2, y2, fill=self.line_color)

    def draw(self, state: State, canvas: EyesCanvas):
        from eye_states import Default, Blinking

        if isinstance(state, Default):
            self._draw_default_state(canvas)
        elif isinstance(state, Blinking):
            self._draw_blinking_state(canvas, state.value)