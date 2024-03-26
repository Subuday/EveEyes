from canvas import Canvas
import sys
from network_client import NetworkClient
from recorder import Recorder
import asyncio

from renderer import Renderer

class EveApp:
    def __init__(self, recorder: Recorder, canvas: Canvas):
        self.renderer = Renderer(canvas)
        self.recorder = recorder
        self.network_client = NetworkClient()

    async def run(self):
        await asyncio.gather(
            asyncio.create_task(self.renderer.run()),
            asyncio.create_task(self.recorder.run()),
            asyncio.create_task(self.network_client.run()),
        )


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
        from canvas import SpiCanvas
        canvas = SpiCanvas(320, 240)
    
    app = EveApp(recorder, canvas)
    
    if sys.platform == "darwin": 
        root.mainloop()
    else:
        asyncio.run(app.run())