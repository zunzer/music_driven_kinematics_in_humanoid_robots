"""
The whole thing
"""
import os
import sys
import numpy as np
import pickle
import threading
from thinking import extract_song_features
from sensing_normalized import deviceInfo, record_to_file, waitForEnd

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

from recognize_posture import PostureRecognitionAgent   #replaced joint_control. 
from dance_keyframes import classic, disco, robotDance

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
            "pop": disco()
        }

        # get the music device that we want to record from
        self.index = deviceInfo()

        # load the classifier and compile it
        with open('../project/music_recognition/NN_classification/svm_model.pkl', 'rb') as f:
            self.music_classifier = pickle.load(f)


        self.recognized = False     #variable if we already recognized a song 
        self.recorded = False       #variable if we already recorded a song  
        self.RecordingThreadAlive = False    #variable if we are currently listening
        self.WaitingThreadAlive = False    #variable if we are currently listening
        self.thread = None          #variable to store a running thread
        self.songStopped = False 
        #self.music_data = extract_song_features("../project/recordings/output_normalized.wav") # TODO: we need 30s long recordings
        #self.music_data = extract_song_features("../project/music_recognition/NN_classification/genres/pop/pop.00000.wav") # TODO: we need 30s long recordings
        print("")
        print('\x1b[6;30;42m' + 'Setup done!' + '\x1b[0m')
        print("")

    def listen(self):
        """
        This records 30s of music and returns it as music_ data
        """
        if not self.recorded and not self.RecordingThreadAlive:                         # nothing was recorded yet and thread is not running
            print("-------------------------------------------------------------------------")
            print('\x1b[1;30;40m' + 'started music recording thread' + '\x1b[0m')
            self.thread = threading.Thread(target=record_to_file, args = (self.index,))
            self.thread.daemon = True
            self.thread.start()
            self.RecordingThreadAlive = True                                            #start thread that waits for music

        if not self.thread.is_alive():           #check if thread finished 
            print('\x1b[1;30;40m' + 'finished music recording and thread closed' + '\x1b[0m')
            self.recorded = True                    #set variable that a recorded file exists  
            self.RecordingThreadAlive = False
            self.music_data = extract_song_features("../project/recordings/output_normalized.wav")
        else: 
            return 

    def think(self, perception):
        """
        get the file from sensing, predict genre from it and set keyframes
        """
        if not self.recognized:
            self.listen()       #start listening to a song or check if a running thread is finished 
            if self.recorded:   #a recorded song exists 
                print("")
                print("Detected a new recorded song, start analyzing...")       #start song processing 
                try:
                    music_input = self.music_data[np.newaxis, :]                #try analyzing, throw error if it fails and start again 
                    prediction = self.music_classifier.predict(music_input)
                    music_genre = self.genres[prediction[0]]
                    print(f"Recognized the following genre: {music_genre}!")
                except: 
                    print('\x1b[3;30;41m' + 'ERROR:' + '\x1b[0m' + '  Song was paused or recording is to short. Please try again!')
                    self.recorded = False
                    return super(DancingAgent, self).think(perception)
               
                keyframes = self.keyframes_dictionary[music_genre]
                self.dance(keyframes)       #start dancing
                self.recorded = False 
                self.recognized = True      
        else:                                                   # if we detected a song, start waiting for end 
            if not self.WaitingThreadAlive:
                print('\x1b[1;30;40m' + 'started waiting thread' + '\x1b[0m')               #start waiting Process 
                self.thread = threading.Thread(target=waitForEnd, args = (self.index,))  
                self.thread.daemon = True
                self.thread.start()
                self.WaitingThreadAlive = True
            
            if not self.thread.is_alive():      #check if waiting thread finished 
                print('\x1b[1;30;40m' + 'song stopped, thread closed' + '\x1b[0m')
                self.WaitingThreadAlive = False
                self.recorded = False  
                self.recognized = False

                # TODO: make robot stop dancing HERE 

                self.keyframes = stand() # robot goes in default standing position
                
        return super(DancingAgent, self).think(perception)

    def dance(self, keyframes):
        """
        This is our acting function. It sets new keyframes to animate if not done yet
        """
        print("")
        print('\x1b[6;30;42m' + 'Start Dancing!' + '\x1b[0m')
        if self.recognized:
            return
        self.keyframes = keyframes


if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '../joint_control'))
    print("Current Working Directory ", os.getcwd())
    #print(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))
    print(sys.path)
    agent = DancingAgent()
    agent.run()
