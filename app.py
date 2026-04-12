import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# LOAD AUDIO
audio, sr = librosa.load("sample.ogg", sr=16000)

# EXTRACT MFCC
mfcc = librosa.feature.mfcc(y=audio,sr=sr,n_mfcc=13)

# CONVERT TO FIXED SIZE
features= np.mean(mfcc.T, axis=0)

print(features.shape)