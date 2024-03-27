from abc import ABC, abstractmethod
import asyncio
import sys
import time
import wave

class Recorder(ABC):
    @abstractmethod
    async def run(self):
        pass

if sys.platform == "darwin":
    class MacOsRecorder(Recorder):
        async def run(self):
            pass
else:
    import alsaaudio

    class AlsaRecorder(Recorder):
        def __init__(self, queue: asyncio.Queue):
            self.pcm = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
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
                num_frames, data = self.pcm.read()
                if num_frames:
                    print(f"Read frames {num_frames} and {len(data)} bytes.")
                    await self.queue.put(data)
                    await asyncio.sleep(0.001)
