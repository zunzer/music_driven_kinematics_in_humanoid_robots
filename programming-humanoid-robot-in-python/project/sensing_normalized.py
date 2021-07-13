'''
Note: You can select the microphone source at the beginning. 
Due to the bad audio quality from microphones, we recommend to use internal recorded sound. 
If it is not possible to set up your microphone successfully, you can load a .waf file from the sond directory. 

WINDOWS: 
    - dont use headphones 
    - pip install pipwin          
            #comment: pipwin == pip, but with optimized packets for windows 
    - pipwin install pyaudio  
        [https://stackoverflow.com/questions/55936179/trying-to-install-pyaudio-using-pip] 

    - Setup the stereomix device in windows, e.g. like this:
        [https://www.howtogeek.com/howto/39532/how-to-enable-stereo-mix-in-windows-7-to-record-audio/]

    - Select stereomix microphone as "Standardaufnahmegerät", run this code and choose Stereomix at the beginning

LINUX: 
    - with conda/pip install portaudio and pyaudio
    - Install voice control using "sudo apt-get install pavucontrol" and run it by using "pavucontrol"
        [https://stackoverflow.com/questions/65079325/problem-with-alsa-in-speech-recognitionpython-3]
    
    - run this file in another terminal and select device "pulse" 
    
    - Select "Monitor of built-in audio" from register card "recordings" in voice control panel 

--> Start and stop music as you like, notice the commandline output  


Sources: 
Code for microphone selection e.g. see: https://stackoverflow.com/questions/40704026/voice-recording-using-pyaudio
Code for recording with pyaudio e.g. see: https://gist.github.com/PandaWhoCodes/9f3dc05faee761149842e43b56e6ee8c
Code for normalization e.g. see: https://www.academis.eu/posts/python_packages/pyaudio/ 
'''

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import os
import time
import shutil


REC_LENGTH = 35                        # length of recorded files
SILENCE_DURATION = 200                 # duration until robot stops dancing if silence
THRESHOLD = 300                        # threshold how loud is silent

FILE_NAME = "output_normalized.wav"    # where to save recorded files
CHUNK_SIZE = 1024                      #recording specific variables
FORMAT = pyaudio.paInt16
RATE = 44100                            
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def check_input(input_string, valid_inputs):
    """
    checks the input for type and value
    """
    selected = input(input_string)
    while True:
        try:
            selected = int(selected)
            if selected not in valid_inputs:
                raise ValueError
            return selected
        except ValueError:
            selected = input("Please enter a valid number: ")


def is_silent(snd_data):
    """
    Returns 'True' if sound data is below the 'silent' threshold
    """
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    """
    Normalize the sound data
    """
    MAXIMUM = 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i * times))
    return r


def trim(snd_data):
    """
    Cut off silence at the beginnign/ending
    """

    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD:
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


def record(index):
    """
    Record music from the selected microphone index for selected time
    """
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=True, input_device_index=index,
                    frames_per_buffer=CHUNK_SIZE)  # start audio recording stream

    snd_started = False  # variable to check if soundrecording started

    r = array('h')  # create sound array
    print("\n")
    print("Please start the music!", end="\r")

    while 1:
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)              # add recorded sample to tone

        silent = is_silent(snd_data)    # check if silent

        if snd_started:         #print how long until recording is finished
            print("Still recording for " + str(abs(round(REC_LENGTH - (time.time() - start_time), 2))) + ' seconds...',
                  end='\r')

        if not silent and not snd_started:  # first detected tone with a higher volume than the treshold
            print("Music detected.                                          ")
            snd_started = True
            start_time = time.time()    # start recording

        if snd_started and (time.time() - start_time) > REC_LENGTH: #check the recorded audio is REC_LENGTH seconds long
            print("Finished recording. ", end="")
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()          # close streams and postprocess audio
    p.terminate()

    r = normalize(r)
    r = trim(r)
    return sample_width, r  # return the results 


def deviceInfo():
    """
    Shows available microphones and allows the user to select one
    """
    audio = pyaudio.PyAudio()
    print("---------------------------record device list----------------------------")
    info = audio.get_host_api_info_by_index(0)
    device_nums = []
    for i in range(info.get('deviceCount')):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
            device_nums.append(i)
    print("-------------------------------------------------------------------------")
    selected = check_input("Select a microphone before starting! Enter device number and press return: ", device_nums)
    return selected 


def load_to_file():
    """
    Loads a file into music processing directory
    """
    print("")
    print("Select a file from sound directory:")
    arr = os.listdir(os.path.join(DIR_PATH, "sounds"))  # print available wav songs
    for i in range(len(arr)):
        if ".wav" in arr[i]:
            print("    |--- " + str(i) + ": " + arr[i])
    print("")

    # check that input is valid
    selected = check_input("Enter a number: ", range(len(arr)))

    if ".wav" in arr[selected]:         # copy the wav file into the processing folder 
        src = os.path.join(DIR_PATH, "sounds", arr[selected])
        dst = os.path.join(DIR_PATH, "recordings", FILE_NAME)
        shutil.copyfile(src, dst)
    else:
        print('\x1b[3;30;41m' + 'Not a .wav file or error occured with selected file' + '\x1b[0m')
        load_to_file()
    return


def record_to_file(index):
    """
    Records from microphone into music processing directory
    """
    path = os.path.join(DIR_PATH, "recordings", FILE_NAME)

    sample_width, data = record(index)      #start recording
    data = pack('<' + ('h' * len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    print("Updated " + FILE_NAME + "       ")   #save recorded file to processing folder
    return


def waitForEnd(index):
    """
    wait until to long silence while the robot dances 
    """
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=1, rate=RATE,
                    input=True, output=True, input_device_index=index,
                    frames_per_buffer=CHUNK_SIZE)

    silence = 0     #variable how long the song was silent
    print("Robot is dancing to current song -- stop music to stop robot ")

    r = array('h')
    while 1:
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        volume_low = is_silent(snd_data)

        if volume_low:          #if volume low, print no tone
            print("--     --                                                           ", end="\r")
            silence += 1
        else:                   #volume high, print tone
            print('--  ' + '\x1b[6;30;42m' + 'ON' + '\x1b[0m' + '  --                  ', end="\r")
            silence = 0
        if silence == 0.4 * SILENCE_DURATION:   #print warning if we reached 40% of the max silence duration
            print("\nMusic stopped, robot will stop dancing in a few seconds")

        if silence > SILENCE_DURATION:
            print("Song finished and robot sleeps!                                                         ")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    return
