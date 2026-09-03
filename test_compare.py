from compare import dtw_distance

user_audio = "samples/user.wav"

reference_audio = "data/reference/hello.wav"

print("Testing Pronunciation Comaprision...")

distance = dtw_distance(user_audio, reference_audio)

print("DTW Comaprision Successful!")
print("DTW Distance:", distance)

# OUTPUT:
#     Your backend successfully did:

#             samples/user.wav
#                     +
#             data/reference/hello.wav
#                     ↓
#             MFCC extraction
#                     ↓
#             Dynamic Time Warping (DTW)
#                     ↓
#             Distance = 67576.74