from gtts import gTTS
import os
import tempfile

# Tamil text sample
tamil_text = "வணக்கம், இது தமிழ் பேச்சு சோதனை. Google Text-to-Speech மூலம் உருவாக்கப்பட்டது."

print("Converting Tamil text to speech using Google TTS...")

# Create gTTS object with Tamil language
tts = gTTS(text=tamil_text, lang='ta', slow=False)

# Save to a temporary file
output_file = "tamil_test.mp3"
tts.save(output_file)

print(f"Successfully created Tamil audio at: {output_file}")

# Play the audio file automatically
print("Playing audio...")
os.startfile(output_file)
