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
        def __init__(self):
            self.pcm = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
                alsaaudio.PCM_NORMAL, 
                channels=2, 
                rate=44100, 
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=256,
                periods=4,
                device="default"
            )
            self.f = wave.open("test.wav", 'wb')
            self.f.setnchannels(2)
            self.f.setsampwidth(2)    #PCM_FORMAT_S16_LE
            self.f.setframerate(44100)

        async def run(self):
            try:
                count = 0
                while True:
                    num_frames, data = self.pcm.read()
                    if num_frames:
                        count += len(data)
                        print(f"Read frames {num_frames} and {len(data)} bytes.")
                        self.f.writeframes(data)
                        await asyncio.sleep(.001)
            except Exception:
                pass
            await asyncio.sleep(10)
            self.stop()
            
        def stop(self):
            self.pcm.close()
            self.f.close()
