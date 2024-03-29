import sys
from canvas import Canvas, SpiCanvas
from eye import Eye
from eyes import Eyes
from time import sleep

class Renderer:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.eyes = Eyes(
            margin_start=43,
            margin_top=89,
            spacing=46,
            rotation_angle=-16,
            eye_width=94,
            eye_height=62,
            eye_num_lines=100
        )

    def run(self):
        from eye_states import Default, Blinking
        while True:
            self.canvas._clear()
            self.eyes.draw(Default(), self.canvas)
            self.canvas._draw()
            sleep(3)
            for i in range(0, 100, 10):
                self.canvas._clear()
                self.eyes.draw(Blinking(i), self.canvas)
                self.canvas._draw()
                if sys.platform == "darwin":
                    sleep(1)

            for i in range(100, 0, -10):
                self.canvas._clear()
                self.eyes.draw(Blinking(i), self.canvas)
                self.canvas._draw()
                if sys.platform == "darwin":
                    sleep(1)


def renderer_main():
    canvas = SpiCanvas(320, 240)
    renderer = Renderer(canvas)
    renderer.run()


