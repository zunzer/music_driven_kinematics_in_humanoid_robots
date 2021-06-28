'''
To install pyaudio on windows (https://stackoverflow.com/questions/55936179/trying-to-install-pyaudio-using-pip): 
- pip install pipwin          #pipwin is the same thing like pip, but with optimized packets for windows 
- pipwin install pyaudio  

Note: Due to the bad audio quality, you can setup the stereomix device in windows like this:
https://www.howtogeek.com/howto/39532/how-to-enable-stereo-mix-in-windows-7-to-record-audio/

Based on: https://stackoverflow.com/questions/40704026/voice-recording-using-pyaudio
'''

import pyaudio
import wave
import os

FORMAT = pyaudio.paInt16
CHANNELS = 2        #Select number of channels 1/2, depends on microphone 
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 30
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

audio = pyaudio.PyAudio()
print("----------------------record device list---------------------")
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
print("-------------------------------------------------------------")

index = int(input("Enter device number and press return: "))  #Note if input function is not working (e.g. in VSCode): Hardcode devicenumber here!

stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,input_device_index = index,
                frames_per_buffer=CHUNK)
print ("Recording...")

Recordframes = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    Recordframes.append(data)
print ("Recording finished")
 
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(DIR_PATH + '/recordings//pyaudio_recording.wav', 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(Recordframes))
waveFile.close()