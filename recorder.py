from abc import ABC, abstractmethod
import sys
import threading
import time
import wave

class Recorder(ABC):

    @abstractmethod
    def start(self):
        pass

if sys.platform == "darwin":
    class MacOsRecorder(Recorder):
        def start(self):
            pass
else:
    import alsaaudio

    class AlsaRecorder(Recorder):
        def __init__(self):
            self.pcm = None
            self.f = wave.open("test.wav", 'wb')
            self.f.setnchannels(2)
            self.f.setsampwidth(2)    #PCM_FORMAT_S16_LE
            self.f.setframerate(44100)

        def _loop(self):
            print("Recoding loop is launched!")
            try:
                count = 0
                while True:
                    num_frames, data = self.pcm.read()
                    if num_frames:
                        count += len(data)
                        print(f"Read frames {num_frames} and {len(data)} bytes.")
                        # print(f"Total bytes - {count}")
                        self.f.writeframes(data)
                        time.sleep(.001)
            except Exception:
                pass

        def start(self):
            self.pcm = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
                alsaaudio.PCM_NORMAL, 
                cardindex=1,
                channels=2, 
                rate=44100, 
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=160,
                periods=4
            )
            threading.Thread(target=self._loop).start()
            time.sleep(10)
            self.stop()
            
        def stop(self):
            self.pcm.close()
            self.f.close()
