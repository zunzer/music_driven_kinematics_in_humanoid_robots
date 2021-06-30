'''
To install pyaudio on windows (https://stackoverflow.com/questions/55936179/trying-to-install-pyaudio-using-pip): 
- pip install pipwin          #pipwin is the same thing like pip, but with optimized packets for windows 
- pipwin install pyaudio  

Note: Due to the bad audio quality, you can setup the stereomix device in windows like this:
https://www.howtogeek.com/howto/39532/how-to-enable-stereo-mix-in-windows-7-to-record-audio/

Based on: https://stackoverflow.com/questions/40704026/voice-recording-using-pyaudio
and: https://gist.github.com/PandaWhoCodes/9f3dc05faee761149842e43b56e6ee8c
'''

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import os
import time

THRESHOLD = 300
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "\\recordings\\output_normalized.wav"
REC_LENGTH = 10
SILENCE_LEN = 300

def is_silent(snd_data):
    '''
    Returns 'True' if below the 'silent' threshold
    '''
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    '''
    Average the volume out
    '''
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    '''
    Trim the blank spots at the start and end
    '''
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def deviceInfo():
    '''
    Shows available microphones and allows the user to select one
    '''
    audio = pyaudio.PyAudio()
    print("----------------------record device list---------------------")
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
    print("-------------------------------------------------------------")
    return int(input("Enter device number and press return: "))  #Note if input function is not working (e.g. in VSCode): Hardcode devicenumber here!


def record(index):
    """
    Record music from the selected microphone until silence
    """

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,input_device_index = index,
        frames_per_buffer=CHUNK_SIZE)

    snd_started = False

    r = array('h')
    print ("-------------------------------------------------------------")
    print ("Please start the music!", end="\r")
    while 1:

        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if snd_started:
            print("Still recording for " + str(round(REC_LENGTH-(time.time()-start_time),2)) + ' seconds...', end='\r')
        
        if not silent and not snd_started:        #first detected tone
            print('Music start detected.    ')
            snd_started = True
            start_time = time.time()

        if snd_started and (time.time()-start_time)>REC_LENGTH:
            print ("Finished recording.                              ")
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    return sample_width, r

def record_to_file(index):
    path = DIR_PATH + FILE_NAME

    sample_width, data = record(index)
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    print("Updated " +FILE_NAME+" -> Call dance thread now")
    waitForEnd(index)

def waitForEnd(index):
    """
    wait until song stopped
    """
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,input_device_index = index,
        frames_per_buffer=CHUNK_SIZE)

    silence = 0
    print("Robot should dance to current song :D")
    
    r = array('h')
    while 1:
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent:
            print("--         --", end="\r")
            silence += 1
        else: 
            print("-- playing --                                                                  ", end="\r")
            silence = 0
        if silence == 0.4*SILENCE_LEN:
            print("               Looks like music finished, robot will stop dancing in a moment..", end="\r")
                
        if silence>SILENCE_LEN:
            print ("Song finished and robot sleeps! -> Make robot do nothing                              ")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    index = deviceInfo()
    while 1:
        record_to_file(index)
