import os
import random

from background_task import background
from gtts import gTTS
from intergalactic.settings import MEDIA_URL
from mainapp.models import Article, VoiceArticle


@background()
def play_text(pk):
    print('start play_text')
    article = Article.objects.get(pk=pk)
    if VoiceArticle.objects.filter(article=article).exists():
        path = str(VoiceArticle.objects.get(article=article).audio_file)
        print(path)
        try:
            os.remove(f"./.{MEDIA_URL}{path}")
        except FileNotFoundError:
            print("Файл отсутствует")
        VoiceArticle.objects.get(article=article).delete()
    text = article.text_audio
    print(text)
    unique_file = "audio_" + str(random.randint(0, 10000)) + ".mp3"
    path = f".{MEDIA_URL}audio/{unique_file}"
    voice = gTTS(text, lang="ru")
    voice.save(path)
    VoiceArticle.objects.create(audio_file=f"audio/{unique_file}", article=article)
