"""
The whole project
"""
import os
import sys
import numpy as np
import pickle
import threading
import warnings

from thinking import extract_song_features      
from sensing_normalized import deviceInfo, record_to_file, waitForEnd, load_to_file, check_input

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)  #ignore deprecaition warning
warnings.filterwarnings("ignore", category=UserWarning)  #ignore Userwarning warning

from recognize_posture import PostureRecognitionAgent  # replaced joint_control.
from dance_keyframes import classic, disco, robotDance, stand, verbeugung, denkerpose


class DancingAgent(PostureRecognitionAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(DancingAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)

        # define what we can recognize and dance to
        self.genres = ['classical', 'metal', 'pop']
        self.keyframes_dictionary = {
            "classical": classic(),
            "metal": robotDance(),
            "pop": disco(),
            "default": verbeugung()
        }

        # get the music device that we want to record from
        self.index = deviceInfo()

        # load the classifier and compile it
        with open('../project/music_recognition/svm_model.pkl', 'rb') as f:
            self.music_classifier = pickle.load(f)

        self.recognized = False  # variable if we already recognized a song
        self.music_genre = "unknown"
        self.recorded = False  # variable if we already recorded a song
        self.RecordingThreadAlive = False  # variable if we are currently listening
        self.WaitingThreadAlive = False  # variable if we are currently listening
        self.thread = None  # variable to store a running thread
        self.selected_input = 0  # variable for input type: 1 = record music/ 2 = load music
        self.always_record = False  # variable if we only want to record music
        self.always_load = False  # variable if we only want to load files
        print("")
        print('\x1b[6;30;42m' + 'Setup done!' + '\x1b[0m')
        print("")

    def setup_sensing_thread(self, index):
        """
        lets user choose between different music input options
        mainly developed to test robots genre recognition without recording songs every time
        """
        if not self.always_record and not self.always_load:

            # Denkerpose not working properly
            #print("Going into denkerpose...")
            #self.keyframes = ([], [], [])
            #self.dance(denkerpose())
            #self.start_time = -1

            
            correct_inputs = [1, 2, 3, 4]
            print("------------------------------ Select Input ------------------------------")
            print("   1: Record song live with selected microphone.")
            print("   2: Load already recorded song from storage.")
            print("   3: Always use option 1. ")
            print("   4: Always use option 2. ")
            print("-------------------------------------------------------------------------")

            self.selected_input = check_input("Enter a number: ", correct_inputs)
            if self.selected_input == 1:  # only record
                record_to_file(index)
            elif self.selected_input == 3:  # always record
                self.selected_input = 1
                self.always_record = True
                record_to_file(index)
            elif self.selected_input == 2:  # only load
                load_to_file()
            elif self.selected_input == 4:  # always load
                self.selected_input = 2
                self.always_load = True
                load_to_file()
        else:
            if self.always_record:  # function to check if there was selected always
                self.selected_input = 1
                record_to_file(index)
            elif self.always_load:
                self.selected_input = 2
                load_to_file()
        return

    def setup_waiting_thread(self, index):
        """
        lets user choose between stop robot together with music or on key down.
        """
        if self.selected_input == 1:
            waitForEnd(index)
        elif self.selected_input == 2:
            input("Press enter to stop robot.")
        else:
            print("Nothing" + str(self.selected_input))
        return

    def listen(self):
        """
        This records music and returns it as music_data
        """

        if not self.recorded and not self.RecordingThreadAlive:  # nothing was recorded yet and thread is not running
            self.thread = threading.Thread(target=self.setup_sensing_thread, args=(self.index,))
            self.thread.daemon = True
            self.thread.start()
            self.RecordingThreadAlive = True  # start thread that waits for music

        if not self.thread.is_alive():  # check if thread finished
            self.recorded = True  # set variable that a recorded file exists
            self.RecordingThreadAlive = False
            self.music_data = extract_song_features("../project/recordings/output_normalized.wav")
        else:
            return

    def think(self, perception):
        """
        get the file from sensing, predict genre from it and set keyframes
        """
        if not self.recognized:
            self.listen()  # start listening to a song or check if we finished recording
            if self.recorded:  # a recorded song exists
                print("")
                print("Detected a new recorded song, start analyzing...")  # start song processing
                try:
                    music_input = self.music_data[np.newaxis, :]  # try analyzing, throw error if it fails and start again
                    prediction = self.music_classifier.predict(music_input)
                    self.music_genre = self.genres[prediction[0]]
                    print(f"Recognized the following genre: {self.music_genre}!")
                except:
                    print(
                        '\x1b[3;30;41m' + 'ERROR:' + '\x1b[0m' + '  Song was paused, overmodulated or recording is to short. Please try again!') #throw error message
                    print("")
                    self.recorded = False
                    return super(DancingAgent, self).think(perception)

                keyframes = self.keyframes_dictionary[self.music_genre] #set the keyframes of the recognized genre
                print("")
                print('\x1b[6;30;42m' + 'Start Dancing!' + '\x1b[0m')
                self.dance(keyframes)  # start dancing
                self.recorded = False  # set variable to false, that we know there is no recorded but not yet classified song
                self.recognized = True  # set variable to true, that we know there is a recognized song
        else:  # if we recognized a song and the robot is already dancing, start waiting for end
            
            # make dancing a loop, so that the robot continues
            if self.keyframes == ([], [], []) and self.recognized and self.music_genre != "unknown":
                print("")
                print("Continue to dance")
                self.keyframes = self.keyframes_dictionary[self.music_genre]

            #if we are not waiting for the end, start a new waiting thread
            if not self.WaitingThreadAlive:
                self.thread = threading.Thread(target=self.setup_waiting_thread, args=(self.index,))
                self.thread.daemon = True
                self.thread.start()
                self.WaitingThreadAlive = True

            if not self.thread.is_alive():  # check if waiting thread finished, the user has stopped the music or pressed enter
                self.WaitingThreadAlive = False
                self.recorded = False
                print('\x1b[0;30;47m' + 'Stopped Dancing!' + '\x1b[0m')
                print("")

                self.start_time = -1
                self.keyframes = ([], [], [])   #stop keyframes
                self.working = False

                self.recognized = False
                keyframes = self.keyframes_dictionary["default"]
                self.dance(keyframes)  # robot goes in default bow and continues with stand position
                self.music_genre = "unknown"

        return super(DancingAgent, self).think(perception)

    def dance(self, keyframes):
        """
        This is our acting function. It sets new keyframes to animate if not done yet
        """
        if self.recognized:
            return
        self.keyframes = keyframes


if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '../joint_control'))
    #print("Current Working Directory ", os.getcwd())
    # print(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))
    #print(sys.path)
    agent = DancingAgent()
    agent.run()
