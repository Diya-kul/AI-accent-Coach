
from features import extract_features
from compare import dtw_distance
from feedback import generate_feedback
from predict import predict_accent
import os
import sys

# user choose a word
'''
need to add audio manually
word = input("Enter word to practice: ").lower()'''

word = 'hello'

user_audio = "Samples/user.wav"

ref_audio= f"data/reference/{word}.wav"

if not os.path.exists(ref_audio):
    print(f"Sorry! NO reference audio found for '{word}")
    sys.exit()

#Pronunciation evaluation
distance = dtw_distance( user_audio, ref_audio)

# convert DTW distance to score
score = max(0, 100 - int(distance/4000))


feedback = generate_feedback(distance)

# RESULT 
print("\n----Accent Coach Result -----")
print("word:", word)
print("DTW Distance: ", distance)
print("Pronunciation score:", score, "/100")
print("Feedback: ",feedback)

#Accent detection
accent = predict_accent(user_audio)
print("Predicted Accent:",accent)