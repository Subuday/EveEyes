from time import sleep
from eye import Eye
from eyes import Eyes
from canvas import Canvas
import threading
import sys

from recorder import Recorder

class EveApp:
    def __init__(self, recorder: Recorder, canvas: Canvas):
        self.recorder = recorder
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

    def _run_rendering(self):
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
                sleep(0.005)

            for i in range(100, 0, -10):
                self.canvas._clear()
                self.eyes.draw(Blinking(i), self.canvas)
                self.canvas._draw()
                sleep(0.005)
    
    def _run_recording(self):
        self.recorder.start()        

    def run(self):
        self._run_rendering()
        self._run_recording()


if __name__ == '__main__':
    if sys.platform == "darwin":
        from recorder import MacOsRecorder
        recorder = MacOsRecorder()
    else:
        from recorder import AlsaRecorder
        recorder = AlsaRecorder()

    if sys.platform == "darwin": 
        import tkinter as tk
        root = tk.Tk()
        root.title('Eve Eyes')
        root.geometry("320x240")
        root.configure(background='#000000')
        
        from canvas import TkinterCanvas
        canvas = TkinterCanvas(root, 320, 240)
    else:
        canvas = SpiCanvas()
    
    app = EveApp(recorder, canvas)

    thread = threading.Thread(target=app.run).start()
    
    if sys.platform == "darwin": 
        root.mainloop()
    else:
        while True:
            pass