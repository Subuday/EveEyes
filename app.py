import wave
from canvas import Canvas
import sys
from network_client import NetworkClient
from recorder import Recorder
import asyncio
from renderer import Renderer
from player import Player
import alsaaudio

class EveApp:
    def __init__(self, canvas: Canvas):
        self.renderer = Renderer(canvas)
        audioQueue = asyncio.Queue()
        self.recorder = EveApp._create_recorder(audioQueue)
        self.player = EveApp._create_player(audioQueue)
        self.network_client = NetworkClient()

    @staticmethod
    def _create_recorder(queue: asyncio.Queue):
        if sys.platform == "darwin":
            from recorder import MacOsRecorder
            recorder = MacOsRecorder()
        else:
            from recorder import AlsaRecorder
            recorder = AlsaRecorder(queue)
        return recorder

    @staticmethod
    def _create_player(queue: asyncio.Queue):
        if sys.platform == "darwin":
            from player import MacOsPlayer
            player = MacOsPlayer()
        else:
            from player import AlsaPlayer
            player = AlsaPlayer(queue)
        return player

    async def run(self):
        await asyncio.gather(
            # asyncio.create_task(self.renderer.run()),
            asyncio.create_task(self.recorder.run()),
            asyncio.create_task(self.player.run()),
            asyncio.create_task(self.network_client.run()),
        )


if __name__ == '__main__':
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
        # canvas = SpiCanvas(320, 240)
        canvas = None

    app = EveApp(canvas)
    
    if sys.platform == "darwin": 
        root.mainloop()
    else:
        asyncio.run(app.run())