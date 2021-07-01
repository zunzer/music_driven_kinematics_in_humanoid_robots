"""
The whole thing
"""
import os
import sys
import numpy as np
import pickle
from thinking import extract_song_features
#from keras.models import load_model
#path = os.path.join(os.path.dirname(__file__), '../joint_control')
#sys.path.insert(1,path)

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))

from joint_control.recognize_posture import PostureRecognitionAgent
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

        # load the classifier and compile it
        with open('../project/music_recognition/NN_classification/svm_model.pkl', 'rb') as f:
            self.music_classifier = pickle.load(f)

        # for now use a random file from the genres train data -- TODO: read the music from sensing in the future
        self.recognized_flag = False
        #self.music_data = extract_song_features("../project/recordings/output_normalized.wav") # TODO: we need 30s long recordings
        #self.music_data = extract_song_features("../project/music_recognition/NN_classification/genres/pop/pop.00000.wav") # TODO: we need 30s long recordings

        print("done setting up everything")

    def listen(self):
        """
        This records 30s of music and returns it as music_ data
        TODO: @Severin, hier sollte dann ein Funktionsaufruf rein, der dein sensing_normalized aufruft oder so
        """
        print("sensing")
        music_data = extract_song_features("../project/music_recognition/NN_classification/genres/pop/pop.00000.wav")
        return music_data

    def think(self, perception):
        """
        get the file from sensing, predict genre from it and set keyframes
        """
        if not self.recognized_flag:
            self.music_data = self.listen()
            music_input = self.music_data[np.newaxis, :]
            prediction = self.music_classifier.predict(music_input)
            music_genre = self.genres[prediction[0]]
            print(f"recognized the following genre: {music_genre}!")

            # TODO: put this into separate act function
            keyframes = self.keyframes_dictionary[music_genre]
            self.dance(keyframes)
            self.recognized_flag = True

        return super(DancingAgent, self).think(perception)

    def dance(self, keyframes):
        """
        This is our acting function. It sets new keyframes to animate if not done yet
        """
        if self.recognized_flag:
            return
        self.keyframes = keyframes


if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '../joint_control'))
    print("Current Working Directory ", os.getcwd())
    #print(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'joint_control'))
    print(sys.path)
    agent = DancingAgent()
    agent.run()
