import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 30  # Duration of recording

def record():
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print("recording...")
    sd.wait()  # Wait until recording is finished
    write('../project/recordings/output.wav', fs, myrecording)  # Save as WAV file
    print("done recording")