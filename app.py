from time import sleep
from eye import Eye
from eyes import Eyes
from eyes_canvas import EyesCanvas, DumbEyesCanvas
import threading
import sys

from recorder import AlsaRecorder, Recorder

class EveApp:
    def __init__(self, recorder: Recorder, canvas: EyesCanvas):
        self.recorder = recorder
        self.canvas = canvas
        self.eyes = Eyes(
            spacing=92,
            rotation_angle=-16,
            eye_width=188,
            eye_height=124,
            eye_num_lines=100
        )

    def _run_rendering(self):
        from eye_states import Default, Blinking
        while True:
            self.eyes.draw(Default(), self.canvas)
            sleep(3)
            for i in range(0, 100, 10):
                self.eyes.draw(Blinking(i), self.canvas)
                sleep(0.005)

            for i in range(100, 0, -10):
                self.eyes.draw(Blinking(i), self.canvas)
                sleep(0.005)
    
    def _run_recording(self):
        self.recorder.start()

    def run(self):
        self._run_recording()


if __name__ == '__main__':
    if sys.platform == "darwin":
        recorder = MacOsRecorder()
    else:
        recorder = AlsaRecorder()

    if sys.platform == "darwin": 
        import tkinter as tk
        root = tk.Tk()
        root.title('Eve Eyes')
        root.geometry("680x340")
        root.configure(background='#000000')

        canvas = tk.Canvas(root, width=680, height=340, bg='black')
        canvas.pack()
    canvas = DumbEyesCanvas()
    
    app = EveApp(recorder, canvas)

    thread = threading.Thread(target=app.run).start()
    
    if sys.platform == "darwin": 
        root.mainloop()
    else:
        while True:
            pass