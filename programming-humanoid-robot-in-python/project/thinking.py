import librosa
import numpy as np

def compress_filter(file):
    y, sr = librosa.load(file)
    x = librosa.mu_compress(y, quantize=False)
    return x, sr

def extract_song_features(file):
    """
    get Mel-frequency cepstral coefficients and normalize
    this is the same as in the notebook,
    maybe we can solve this a bit more elegantly than implementing it twice at one point
    """
    #y, _ = librosa.load(file)
    y, sr = compress_filter(file)
    mfcc = librosa.feature.mfcc(y)
    mfcc /= np.amax(np.absolute(mfcc))
    return np.ndarray.flatten(mfcc)[:25000]