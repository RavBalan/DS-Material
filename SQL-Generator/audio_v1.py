import wave
import time
import pyaudio
from groq import Groq

client = Groq(api_key="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")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
AUDIO_PATH = "live_input.wav"

def record_audio_to_file(path: str):
    """Record audio from the microphone and save to a file."""
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("🎙️ Recording...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("🛑 Done.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def transcribe_audio_file(audio_path: str):
    """Transcribe audio using Groq Whisper Turbo."""
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            response_format="text",
            language="en",
            prompt="The audio is a customer service phone call discussing product issues or inquiries."
        )
        return transcription

def main():
    while True:
        record_audio_to_file(AUDIO_PATH)
        text = transcribe_audio_file(AUDIO_PATH)
        print(f"\n📝 Transcription:\n{text}\n")
        time.sleep(1)  # optional pause

if __name__ == "__main__":
    main()
