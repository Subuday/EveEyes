from abc import ABC, abstractmethod
from multiprocessing import Queue
import sys
import time
import wave

class Recorder(ABC):
    @abstractmethod
    def run(self):
        pass

if sys.platform == "darwin":
    class MacOsRecorder(Recorder):
        def run(self):
            pass
else:
    import alsaaudio

    class AlsaRecorder(Recorder):
        def __init__(self, queue: Queue):
            self.pcm = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
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
                num_frames, data = self.pcm.read()
                if num_frames:
                    print(f"Read frames {num_frames} and {len(data)} bytes.")
                    self.queue.put(data)


def recorder_main(queue: Queue):
    recorder = AlsaRecorder(queue)
    recorder.run()
