from abc import ABC, abstractmethod
import asyncio
import alsaaudio
import sys
import wave

class Player(ABC):
    @abstractmethod
    async def run(self):
        pass

if sys.platform == "darwin":
    class MacOsPlayer(Player):
        async def run(self):
            pass
else:
    import alsaaudio

    class AlsaPlayer(Player):
        def __init__(self, queue: asyncio.Queue):
            self.pcm = alsaaudio.PCM(
                alsaaudio.PCM_PLAYBACK,
                alsaaudio.PCM_NORMAL, 
                channels=2, 
                rate=44100, 
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=2048,
                device="plughw:1,0"
            )
            self.queue = queue

        async def run(self):
            while True:
                data = await self.queue.get()
                print(f"Write {len(data)} bytes.")
                self.pcm.write(data)
                await asyncio.sleep(0.001)
