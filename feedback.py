def generate_feedback(distance):
    if distance < 40000:
        return "Excellent pronunciation! Your speech closely matches the native reference."
    elif distance < 70000:
        return "Good pronunciation. Minor improvements in clarity and timing may help"
    elif distance <100000:
        return "Fail pronunciation. Try matching the pronunciation speed and stress pattern."
    else:
        "Needs improvement. Practice the word again and listen carefully to the reference audio"