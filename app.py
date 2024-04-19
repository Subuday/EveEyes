import wave
from canvas import Canvas
import sys
from network_client import network_client_main
from renderer import renderer_main
from media_manager import media_manager_main
import asyncio
from multiprocessing import Process, Queue

class EveApp:
    def __init__(self):
        self.renderer_process = Process(target=renderer_main)
        output_queue = Queue()
        input_queue = Queue()
        self.media_manager_process = Process(target=media_manager_main, args=(output_queue,))
        self.network_client_process = Process(target=network_client_main, args=(input_queue, output_queue))

    async def run(self):
        self.media_manager_process.start()
        self.renderer_process.start()
        self.network_client_process.start()

        self.media_manager_process.join()
        self.renderer_process.join()
        self.network_client_process.join()


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
