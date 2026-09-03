from feedback import generate_feedback

distance = 67576.74531673927

print("Testing Feedback Generation...")

feedback = generate_feedback(distance)

print("DTW Distance:", distance)
print("Feedback:", feedback)