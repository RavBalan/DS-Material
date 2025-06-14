# client = Groq(api_key="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")
import os
import wave
import pyaudio
import subprocess
from groq import Groq
import tempfile

# Initialize Groq client
client = Groq(api_key="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")

def record_audio(file_path, sample_rate=16000, channels=1, chunk=1024, record_seconds=10):
    """Record audio from microphone and save as WAV file."""
    try:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk
        )
        
        print("Recording... Speak now.")
        frames = []
        
        for _ in range(0, int(sample_rate / chunk * record_seconds)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
        
        print("Recording stopped.")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
    except Exception as e:
        print(f"Error during recording: {str(e)}")
        raise

def preprocess_audio(input_path, output_path):
    """Preprocess audio to 16kHz mono FLAC using FFmpeg."""
    try:
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Adjust to your FFmpeg path
        subprocess.run([
            ffmpeg_path, "-i", input_path, "-ar", "16000", "-ac", "1",
            "-c:a", "flac", output_path
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error preprocessing audio: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("FFmpeg not found. Ensure FFmpeg is installed and added to PATH or specify the full path.")
        return False

def transcribe_audio(audio_path):
    """Transcribe audio using Groq's Whisper API."""
    try:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                response_format="text",
                language="en",
                prompt="The audio is a customer service phone call discussing product issues or inquiries."
            )
            return transcription
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return None

def main():
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav, \
             tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as temp_flac:
            
            wav_path = temp_wav.name
            flac_path = temp_flac.name
            
            record_audio(wav_path, record_seconds=10)
            
            if not preprocess_audio(wav_path, flac_path):
                print("Failed to preprocess audio.")
                return
            
            transcription = transcribe_audio(flac_path)
            if transcription:
                print("\nTranscription Result:")
                print(transcription)
            else:
                print("Transcription failed.")
            
            os.remove(wav_path)
            os.remove(flac_path)
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    if not os.environ.get("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable not set.")
    else:
        main()