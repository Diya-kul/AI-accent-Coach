
def generate_feedback(distance):
    
    if distance > 50:
        return "Good pronunciation"
    elif distance > 100:
        return "Almost correct, improve clarity"
    else:
        return "Needs improvement"