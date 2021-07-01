"""
The whole thing
"""
import os
import sys
import numpy as np
import pickle
import threading
import time
from thinking import extract_song_features
from sensing_normalized import deviceInfo, record_to_file
from simple_sensing import record

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))

from recognize_posture import PostureRecognitionAgent
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
        self.recognized = False
        self.listened = False
        self.threadAlive = False
        self.thread = None
        #self.music_data = extract_song_features("../project/recordings/output_normalized.wav") # TODO: we need 30s long recordings
        #self.music_data = extract_song_features("../project/music_recognition/NN_classification/genres/pop/pop.00000.wav") # TODO: we need 30s long recordings

        print("Done with setup")

    def listen(self):
        """
        This records 30s of music and returns it as music_ data
        TODO: @Seraphin, hier sollte dann ein Funktionsaufruf rein, der dein sensing_normalized aufruft oder so
        """
        if not self.listened:
            print("Started thread")
            # TODO: do this in the background (only if we have something to do in the meantime)
            self.thread = threading.Thread(target=record_to_file, args = (self.index,))
            self.thread.start()
            self.threadAlive = True
            #record()
        #music_data = extract_song_features("../project/recordings/output_normalized.wav")
        if not self.thread.is_alive():
            print("Finished Thread")
            music_data = extract_song_features("../project/recordings/output.wav")
            return music_data
        else: 
            return 

    def think(self, perception):
        """
        get the file from sensing, predict genre from it and set keyframes
        """
        if not self.recognized and not self.threadAlive:
            self.music_data = self.listen()
            if not self.threadAlive:
                music_input = self.music_data[np.newaxis, :]
                prediction = self.music_classifier.predict(music_input)
                music_genre = self.genres[prediction[0]]
                print(f"recognized the following genre: {music_genre}!")

            # TODO: put this into separate act function
                keyframes = self.keyframes_dictionary[music_genre]
                self.dance(keyframes)
                self.recognized = True
                time.sleep(5000)
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
    print("Current Working Directory ", os.getcwd())
    #print(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))
    print(sys.path)
    agent = DancingAgent()
    agent.run()
