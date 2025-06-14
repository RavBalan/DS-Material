import os
import tempfile
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
from groq import Groq
from gtts import gTTS
import pyglet

# === CONFIG ===
groq_api_key = "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"  # replace this

client = Groq(api_key=groq_api_key)

def record_audio(duration=5, samplerate=44100):
    print("🎤 Recording... Speak now.")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("✅ Done recording.")
    
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    scipy.io.wavfile.write(temp_file.name, samplerate, audio)
    return temp_file.name

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            response_format="text",
            language="en"
        )
    return transcription

def get_groq_response(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "speech_output.mp3"
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    player = pyglet.media.Player()
    player.queue(music)
    player.play()
    pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), music.duration)
    pyglet.app.run()

# === MAIN LOOP ===
if __name__ == "__main__":
    while True:
        print("\n🎙️ Press Enter to talk (or type 'exit' to quit):")
        command = input()
        if command.lower() == 'exit':
            break

        audio_path = record_audio(duration=5)
        try:
            user_text = transcribe_audio(audio_path)
            print(f"🗣️ You said: {user_text}")

            bot_response = get_groq_response(user_text)
            print(f"🤖 Groq: {bot_response}")

            speak_text(bot_response)

        except Exception as e:
            print(f"⚠️ Error: {e}")
