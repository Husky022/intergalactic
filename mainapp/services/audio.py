import random
from gtts import gTTS
from intergalactic.settings import MEDIA_URL


def play_text(article):
    text = article.text_audio
    unique_file = "audio_" + str(random.randint(0, 10000)) + ".mp3"
    path = f".{MEDIA_URL}audio/{unique_file}"
    voice = gTTS(text, lang="ru")
    voice.save(path)
    return unique_file
