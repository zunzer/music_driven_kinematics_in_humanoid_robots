"""
The whole thing
"""
import librosa
import numpy as np
from keras.models import load_model

from joint_control.recognize_posture import PostureRecognitionAgent


class DancingAgent(PostureRecognitionAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(DancingAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)

        # define what we can recognize and dance to
        self.genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']

        # load the classifier and compile it -- TODO: gives a lot of warnings, probably due to version of tensorflow
        self.music_classifier = load_model('../project/music_recognition/model.h5')
        self.music_classifier.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

        # for now use a random file from the genres train data -- TODO: read the music from sensing in the future
        music_data = self.extract_song_features("../project/recordings/lowdown.wav")
        self.music_file = music_data[np.newaxis, :]

        print("done setting up everything")

    def think(self, perception):
        """
        get the file from sensing, predict genre from it and set keyframes
        """
        scores = self.music_classifier.predict(self.music_file, verbose=0)
        music_genre = self.genres[scores.argmax(axis=-1)[0]]
        print(f"recognized the following genre: {music_genre}!")
        # TODO: here we need a dictionary for the keyframes
        # self.keyframes = frames[music_genre]
        return super(DancingAgent, self).think(perception)

    def extract_song_features(self, f):
        """
        get Mel-frequency cepstral coefficients and normalize
        this is the same as in the notebook,
        maybe we can solve this a bit more elegantly than implementing it twice at one point
        """
        y, _ = librosa.load(f)
        mfcc = librosa.feature.mfcc(y)
        mfcc /= np.amax(np.absolute(mfcc))
        return np.ndarray.flatten(mfcc)[:25000]


if __name__ == '__main__':
    agent = DancingAgent()
    agent.run()
