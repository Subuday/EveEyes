import alsaaudio
import sys
import wave

f = wave.open("music.wav", 'rb')

print('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                            f.getframerate()))

# 8bit is unsigned in wav files
if f.getsampwidth() == 1:
    format = alsaaudio.PCM_FORMAT_U8
# Otherwise we assume signed data, little endian
elif f.getsampwidth() == 2:
    format = alsaaudio.PCM_FORMAT_S16_LE
elif f.getsampwidth() == 3:
    format = alsaaudio.PCM_FORMAT_S24_LE
elif f.getsampwidth() == 4:
    format = alsaaudio.PCM_FORMAT_S32_LE
else:
    raise ValueError('Unsupported format')

periodsize = f.getframerate() // 8

device = alsaaudio.PCM(
    channels=f.getnchannels(),
    rate=f.getframerate(), 
    format=format, 
    periodsize=periodsize,
    device="plughw:1,0"
)

data = f.readframes(periodsize)
while data:
    # Read data from stdin
    device.write(data)
    data = f.readframes(periodsize)

f.close()