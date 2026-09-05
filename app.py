from backend.compare import dtw_distance
from backend.feedback import generate_feedback
from backend.predict import predict_accent

import os
import sys

# user choose a word
word = 'hello'

# AUDIO PATHS
user_audio = "Samples/user.wav"
ref_audio= f"data/reference/{word}.wav"

# Check if user audio exists
if not os.path.isfile(user_audio):
    print(f"User audio file not found: {user_audio}")
    sys.exit()


# Check if reference audio exists
if not os.path.isfile(ref_audio):
    print(f"No reference audio found for '{word}'")
    sys.exit()

print("Analyzing your pronunciation....\n")


# 1. Pronunciation evaluation using DTW
distance = dtw_distance( user_audio, ref_audio)

# 2. convert DTW distance to score
score = max(0, 100 - int(distance/4000))

# 3. Generate Feedback
feedback = generate_feedback(distance)

# 4. Detect accent
accent = predict_accent(user_audio)


# Display results
print("---------- AI ACCENT COACH RESULT ----------")
print(f"Word: {word}")
print(f"Predicted Accent: {accent}")
print(f"DTW Distance: {distance:.2f}")
print(f"Pronunciation Score: {score}/100")
print(f"Feedback: {feedback}")
print("--------------------------------------------")


