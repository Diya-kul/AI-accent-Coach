from features import extract_features

audio_path = "samples/user.wav"

features = extract_features(audio_path)

if features is not None:
    print("Feature Extraction successful!")
    print("Feature shape: ", features.shape)
    print("Features: ", features)

else:
    print("Feature extraction failed.")
    
# OUTPUT OF THIS FILE:
#     ✅ Audio file is loading correctly
#     ✅ Librosa is working
#     ✅ MFCC extraction is working
#     ✅ 30 features are being generated