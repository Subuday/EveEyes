from abc import ABC, abstractmethod
from PIL import Image, ImageDraw
import sys

class Canvas(ABC):

    def __init__(self, width, height):
        self.default_color = 0
        self.image = Image.new("RGB", (width, height), self.default_color)
        self.draw = ImageDraw.Draw(self.image)

    def draw_line(self, x1, y1, x2, y2, fill):
        self.draw.line([(x1, y1), (x2, y2)], fill=fill, width=1)

    @abstractmethod
    def _draw(self):
        pass

    def _clear(self):
        self.image.paste(self.default_color, box=[0, 0, self.image.size[0], self.image.size[1]])

if sys.platform == "darwin":
    import tkinter as tk
    from PIL import ImageTk

    class TkinterCanvas(Canvas):
        def __init__(self, root, width, height):
            super().__init__(width, height)
            self.canvas = tk.Canvas(root, width=width, height=height)
            self.canvas.pack()
            self.tk_image = None

        def _draw(self):
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)
else:
    from LCD_2inch4 import LCD_2inch4

    class SpiCanvas(Canvas):
        def __init__(self, width, height):
            super().__init__(width, height)
            self.canvas = LCD_2inch4()
            self.canvas.Init()
            self.canvas.clear()
            self.canvas.bl_DutyCycle(50)

        def _draw(self):
            image = self.image.rotate(90, expand=True)
            self.canvas.ShowImage(image)
