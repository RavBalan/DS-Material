# groq_api_key = "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"  

import tempfile
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
from groq import Groq
import pyttsx3
import speech_recognition as sr
import time

groq_api_key = "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"
client = Groq(api_key=groq_api_key)

engine = pyttsx3.init()
recognizer = sr.Recognizer()
mic = sr.Microphone()

def record_audio(duration=3, samplerate=44100):
    print("Recording command...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("Done recording.")
    
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
    return transcription.strip()

def get_groq_response(messages):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )
    return response.choices[0].message.content

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word(wake_words=("vektorr", "vector", "victor")):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        audio = recognizer.listen(source, phrase_time_limit=3)
    try:
        spoken_text = recognizer.recognize_google(audio).lower()
        print(f"Heard: {spoken_text}")
        return any(word in spoken_text for word in wake_words)
    except sr.UnknownValueError:
        print("Didn't catch anything.")
        return False
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return False

context=  { "role": "system", 
            "content": f"""
            You are an AI assistant for a Audio. You Don't reval your a language model. your name is vektorr. """
        }


if __name__ == "__main__":
    chat_history = [context]

    while True:
        if listen_for_wake_word():
            print("Wake word detected! Starting 5-minute session...")
            start_time = time.time()
            speak_text('Hey How can i help you..')        

            while time.time() - start_time < 300:
                audio_path = record_audio(duration=5)

                try:
                    user_text = transcribe_audio(audio_path).strip()

                    if not user_text or user_text.strip(". ").strip() == "":
                        print("Silence or placeholder detected, skipping...")
                        continue
                    
                    if "bye" in user_text.lower():
                        print("Bye! Exiting program...")
                        speak_text("Goodbye! Have a great day.")
                        break  
                
                    print(f"You said: {user_text}")
                    chat_history.append({"role": "user", "content": user_text})

                    bot_response = get_groq_response(chat_history)
                    print(f"Alita: {bot_response}")

                    chat_history.append({"role": "assistant", "content": bot_response})
                    speak_text(bot_response)

                except Exception as e:
                    print(f"Error: {e}")
