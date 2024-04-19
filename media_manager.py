from eve_media import App
from multiprocessing import Queue
import threading

class MediaManager():
    def __init__(self, queue: Queue):
        self.app = App.instance()
        self.queue = queue

    def run(self):
        self.app.start()
        while True:
            data = self.queue.get()
            if data:
                print("Data is written!")
                self.app.media_manager().write(data)



def media_manager_main(queue: Queue):
    media_manager = MediaManager(queue)
    media_manager.run()
