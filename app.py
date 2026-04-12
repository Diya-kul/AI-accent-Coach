import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

# Feature Extraction Function
def extract_features(file_path):
    try:
        # LOAD AUDIOS
        audio, sr= librosa.load(file_path, sr=16000) #why 16000 frequency
        
        # CHECK IF AUDIO IS EMPTY
        if len(audio) == 0:
            print("Empty audio: ", file_path)
            return None
    
        # EXTRACR MFCC
        mfcc= librosa.feature.mfcc( y=audio, sr=sr, n_mfcc=13) #iss line ka kya mtlab ha?
    
        # CONVERT TO FIXED SIZE
        return np.mean(mfcc.T, axis=0)
    except Exception as e:
        print("Error loading.... ")
        print(e)
        return None

# Create Dataset (X and y)
x=[]
y=[]
'''
    LABELS:
        0 = indian_accent
        1 = British_accent
        2 = American_accent
'''
def files(child_directory):
    parent_directory = "data"
    return os.path.join(parent_directory, child_directory)

bad_files=[]

for file in os.listdir(files("indian_accent")):
    file_path= os.path.join(files("indian_accent"),file)
    features= extract_features(file_path)

    if features is not None:    
        x.append(features)
        y.append(0)
    else:
        bad_files.append(file_path)
    
for file in os.listdir(files("British_accent")):
    file_path= os.path.join(files("British_accent"),file)
    features= extract_features(file_path)

    if features is not None:    
        x.append(features)
        y.append(1)
    else:
        bad_files.append(file_path)
    
for file in os.listdir(files("American_accent")):
    file_path= os.path.join(files("American_accent"),file)
    features= extract_features(file_path)

    if features is not None:    
        x.append(features)
        y.append(2)
    else:
        bad_files.append(file_path)
        
print("!!!!!!!! \n Delete Bad files: ", bad_files)

# TRANING MODEL
model= RandomForestClassifier()
model.fit(x,y)

print("Modeltrained successfull!")

# TEST THE MODEL 
test_file= "sample.ogg"

features= extract_features(test_file)
prediction= model.predict([features])

if prediction[0] == 0:
    print("Indian accent")
elif prediction[0]==1:
    print("British accent")
else:
    print("American accent")