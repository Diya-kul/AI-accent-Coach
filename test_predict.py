from predict import predict_accent

audio_path = "samples/user.wav"

print("Testing Accent Prediction...")
print()

accent = predict_accent(audio_path)

print("Predicted Accent: ", accent)

# OUTPUT:
#     Model loads successfully
#     Scaler works
#     Features match the model's expected input
#     Prediction is returned successfully