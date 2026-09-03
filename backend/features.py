import librosa
import numpy as np

# Feature Extraction Function
def extract_features(file_path):
    try:
        # LOAD AUDIOS
        audio, sr= librosa.load(file_path, sr=16000) #why 16000 frequency
        
        # CHECK IF AUDIO IS EMPTY
        if len(audio) == 0:
            print(" Empty audio!=: ", file_path)
            return None
    
        # EXTRACR MFCC
        mfcc= librosa.feature.mfcc( y=audio, sr=sr, n_mfcc=30) #iss line ka kya mtlab ha?
    
        # CONVERT TO FIXED SIZE
        return np.mean(mfcc.T, axis=0)
    
    except Exception as e:
        print("! Error loading.... ", file_path)
        print(e)
        return None