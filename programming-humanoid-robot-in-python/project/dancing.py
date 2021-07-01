"""
The whole thing
"""
import numpy as np
import pickle
from thinking import extract_song_features
#from keras.models import load_model

from joint_control.recognize_posture import PostureRecognitionAgent
from keyframes import classic, disco, robotDance

class DancingAgent(PostureRecognitionAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(DancingAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)

        # define what we can recognize and dance to
        self.genres = ['classical', 'metal', 'pop']

        # load the classifier and compile it
        with open('../project/music_recognition/NN_classification/svm_model.pkl', 'rb') as f:
            self.music_classifier = pickle.load(f)

        # for now use a random file from the genres train data -- TODO: read the music from sensing in the future
        self.recognized_flag = False
        self.music_data = extract_song_features("../project/recordings/lowdown.wav")

        print("done setting up everything")

    def think(self, perception):
        """
        get the file from sensing, predict genre from it and set keyframes
        """
        if not self.recognized_flag:
            music_input = self.music_data[np.newaxis, :]
            prediction = self.music_classifier.predict(music_input)
            music_genre = self.genres[prediction[0]]
            print(f"recognized the following genre: {music_genre}!")

            # TODO: here we need a dictionary for the keyframes
            keyframes_dictionary = {
                "classical": classic(),
                "metal": robotDance(),
                "pop": disco()
            }

            self.keyframes = keyframes_dictionary[music_genre]

            self.recognized_flag = True
        return super(DancingAgent, self).think(perception)



if __name__ == '__main__':
    agent = DancingAgent()
    agent.run()
