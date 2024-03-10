from eye import Eye
import tkinter as tk


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

    def draw(self, state: Eye.State, canvas: tk.Canvas):
        canvas.delete('all')
        self.eye1.draw(state, canvas)
        self.eye2.draw(state, canvas)