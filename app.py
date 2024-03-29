import wave
from canvas import Canvas
import sys
from network_client import NetworkClient
from recorder import recorder_main
import asyncio
from renderer import renderer_main
from player import player_main
import alsaaudio
import multiprocessing
from multiprocessing import Process

class EveApp:
    def __init__(self):
        self.renderer_process = Process(target=renderer_main)
        self.audioQueue = multiprocessing.Queue()
        self.player_process = Process(target=player_main, args=(self.audioQueue,))
        self.recorder_process = Process(target=recorder_main, args=(self.audioQueue,))
        outputQueue = asyncio.Queue()
        # self.player = EveApp._create_player(outputQueue)
        self.network_client = NetworkClient(None, outputQueue)

    async def run(self):
        self.player_process.start()
        self.recorder_process.start()
        self.renderer_process.start()
        # await asyncio.gather(
        #     asyncio.create_task(self.network_client.run()),
        # )
        self.player_process.join()
        self.recorder_process.join()
        self.renderer_process.join()


async def main():
    app = EveApp()
    await app.run()

if __name__ == '__main__':
    if sys.platform == "darwin": 
        import tkinter as tk
        root = tk.Tk()
        root.title('Eve Eyes')
        root.geometry("320x240")
        root.configure(background='#000000')
        
        from canvas import TkinterCanvas
        canvas = TkinterCanvas(root, 320, 240)

    if sys.platform == "darwin": 
        root.mainloop()
    else:
        asyncio.run(main())