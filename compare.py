import librosa
import numpy as np

def dtw_distance( user_audio, ref_audio):
    y1, sr1 = librosa.load( user_audio, sr=16000)
    y2, sr2 = librosa.load( ref_audio, sr=16000)
    
    mfcc1 = librosa.feature.mfcc( y=y1, sr=sr1, n_mfcc=13)
    mfcc2 = librosa.feature.mfcc( y=y2, sr=sr2, n_mfcc=13)
    
    #DTW Comparison
    D, wp = librosa.sequence.dtw( X=mfcc1, Y=mfcc2, metric='euclidean')
    
    return D[-1,-1] #final distance
