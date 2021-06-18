#TODO: Recognize and read the music from computer microphone (played by external device)

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 30  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('recordings/output.wav', fs, myrecording)  # Save as WAV file


# [4.53e-03 5.67e-01 8.29e-04 1.10e-04 6.12e-03 1.70e-01 2.06e-04 3.79e-04 2.51e-01 1.12e-04]
# [4.53e-03 5.67e-01 8.29e-04 1.10e-04 6.12e-03 1.70e-01 2.06e-04 3.79e-04 2.51e-01 1.12e-04]