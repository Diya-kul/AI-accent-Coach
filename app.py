
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




'''
Perfect — that’s enough. If the Sound Recorder app exists and works, your microphone is very likely ready for recording. Now we can add **live voice recording** to your app 🎙️

## Step 1: Install required libraries

Open terminal in your project folder and run:

```bash
pip install sounddevice soundfile
```

---

## Step 2: Create `record.py`

Create a new file named:

```txt id="v06xom"
record.py
```

Add this code:

```python
import sounddevice as sd
import soundfile as sf

def record_audio(filename="Samples/user.wav", duration=3, sample_rate=16000):

    print("🎙 Recording... Speak now!")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )

    sd.wait()

    sf.write(filename, audio, sample_rate)

    print("✅ Recording complete!")
```

What this does:

* Records for **3 seconds**
* Saves automatically to:

```txt id="3z89x4"
Samples/user.wav
```

* Uses the correct sample rate (`16000`) for your model.

---

## Step 3: Update `app.py`

Replace your current code with this:

```python
from compare import dtw_distance
from feedback import generate_feedback
from predict import predict_accent
from record import record_audio

import os
import sys

# User chooses word
word = input("Enter word to practice: ").lower()

ref_audio = f"data/reference/{word}.wav"

# Check if reference file exists
if not os.path.isfile(ref_audio):
    print(f"❌ Sorry! No reference audio found for '{word}'")
    sys.exit()

# Record user audio
record_audio()

user_audio = "Samples/user.wav"

# Pronunciation evaluation
distance = dtw_distance(user_audio, ref_audio)

score = max(0, 100 - int(distance / 4000))

feedback = generate_feedback(distance)

print("\n--- Accent Coach Result ---")
print("Word:", word)
print("DTW Distance:", distance)
print("Pronunciation Score:", score, "/100")
print("Feedback:", feedback)

# Accent detection
accent = predict_accent(user_audio)
print("Predicted Accent:", accent)
```

---

## What should happen now

Run:

```bash
python app.py
```

You should see:

```txt id="agjlwm"
Enter word to practice: hello
```

Type:

```txt id="4d3n0g"
hello
```

Then:

```txt id="0p8r5s"
🎙 Recording... Speak now!
```

Say:

```txt id="20pp6v"
hello
```

After 3 seconds:

```txt id="skz2e0"
✅ Recording complete!
```

Then your score + feedback appears automatically.

This is a **big milestone** — your app becomes interactive for the first time.

Try it and tell me **exactly what happens** (including any errors).

'''