"""
The whole thing
"""
import os
import sys
import numpy as np
import pickle
import threading
from thinking import extract_song_features
from sensing_normalized import deviceInfo, record_to_file
from simple_sensing import record

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

        # for now use a random file from the genres train data -- TODO: read the music from sensing in the future
        self.recognized = False     #variable if we already recognized a song 
        self.listened = False       #variable if we already recorded a song  
        self.threadAlive = False    #variable if we are currently listening
        self.thread = None          #variable to store a running thread
        #self.music_data = extract_song_features("../project/recordings/output_normalized.wav") # TODO: we need 30s long recordings
        #self.music_data = extract_song_features("../project/music_recognition/NN_classification/genres/pop/pop.00000.wav") # TODO: we need 30s long recordings
        print("Done with setup")

    def listen(self):
        """
        This records 30s of music and returns it as music_ data
        TODO: @Seraphin, hier sollte dann ein Funktionsaufruf rein, der dein sensing_normalized aufruft oder so
        """
        if not self.listened and not self.threadAlive:
            print("Started music recording thread")
            # TODO: do this in the background (only if we have something to do in the meantime)
            self.thread = threading.Thread(target=record_to_file, args = (self.index))
            self.thread.start()
            self.threadAlive = True

        if not self.thread.is_alive(): #check if thread finished 
            print("Finished music recording, thread closed")
            self.listened = True #set variable to process music 
            self.music_data = extract_song_features("../project/recordings/output_normalized.wav")
        else: 
            return 

    def think(self, perception):
        """
        get the file from sensing, predict genre from it and set keyframes
        """
        if not self.recognized:
            self.listen()       #start listening, or check if the thread is finished 
            if self.listened:
                print("Detected recorded song, start recognizing")  #start song processing 
                music_input = self.music_data[np.newaxis, :]
                prediction = self.music_classifier.predict(music_input)
                music_genre = self.genres[prediction[0]]
                print(f"recognized the following genre: {music_genre}!")
                # TODO: put this into separate act function
                keyframes = self.keyframes_dictionary[music_genre]
                self.dance(keyframes)       #start dancing 
                self.recognized = True      # stop loop
                                            # TODO: dont stop the loop here, instead start over again 
        print("", end="\r")
        return super(DancingAgent, self).think(perception)

    def dance(self, keyframes):
        """
        This is our acting function. It sets new keyframes to animate if not done yet
        """
        print("Start dancing")
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
