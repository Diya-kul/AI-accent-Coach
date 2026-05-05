
from features import extract_features
from compare import dtw_distance
from feedback import generate_feedback
from predict import predict_accent

user_audio = "Samples/user.wav"
ref_audio= "data/reference/hello.wav"

#Pronunciation feedback
distance = dtw_distance( user_audio, ref_audio)
feedback = generate_feedback(distance)

print("DTW Distance: ", distance)
print("Feedback: ",feedback)

#Accent detection
accent = predict_accent(user_audio)