import pyglet
from gtts import gTTS

def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    filename = "speech_output.mp3"
    tts.save(filename)

    music = pyglet.media.load(filename, streaming=False)
    player = pyglet.media.Player()
    player.queue(music)
    player.play()

    def close_app(dt):
        pyglet.app.exit()

    pyglet.clock.schedule_once(close_app, music.duration)
    pyglet.app.run()

if __name__ == "__main__":
    speak_text("All bills have been processed successfully.")
