from time import sleep
import tkinter as tk
from eye import Eye
from eyes import Eyes
import threading

class EveApp:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.eyes = Eyes(
            spacing=92,
            rotation_angle=-16,
            eye_width=188,
            eye_height=124,
            eye_num_lines=100
        )

    def run(self):
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


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Eve Eyes')
    root.geometry("680x340")
    root.configure(background='#000000')

    canvas = tk.Canvas(root, width=680, height=340, bg='black')
    canvas.pack()

    app = EveApp(canvas)

    threading.Thread(target=app.run).start()
    
    root.mainloop()