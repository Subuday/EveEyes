from abc import ABC, abstractmethod
from multiprocessing import Queue
import alsaaudio
import sys
import wave

class Player(ABC):
    @abstractmethod
    def run(self):
        pass

if sys.platform == "darwin":
    class MacOsPlayer(Player):
        def run(self):
            pass
else:
    import alsaaudio

    class AlsaPlayer(Player):
        def __init__(self, queue: Queue):
            self.pcm = alsaaudio.PCM(
                alsaaudio.PCM_PLAYBACK,
                alsaaudio.PCM_NORMAL, 
                channels=2, 
                rate=44100, 
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=8192,
                device="plughw:1,0"
            )
            self.queue = queue

        def run(self):
            while True:
                data = self.queue.get()
                print(f"Write {len(data)} bytes.")
                self.pcm.write(data)



def player_main(queue: Queue):
    player = AlsaPlayer(queue)
    player.run()
