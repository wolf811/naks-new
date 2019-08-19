from django.core.management.base import BaseCommand
from mixer.backend.django import mixer
from mainapp.models import *
import random

news_titles = [
    'Конференция НАКС',
    'Общее собрание',
    'Семинар НАКС',
    'Вебинар НАКС',
    'Съезд НАКС',
    'Открытие центра',
    'Заключение соглашения',
    'Новая редакция нормативного документа'
]



class Command(BaseCommand):
    def handle(self, *args, **options):
        Post.objects.all().delete()

        for i in range(8):
            mixer.blend(
                Post,
                title = news_titles[i],
                active = True if random.randint(0, 100) > 50 else False,
            )
            print('creating posts:', news_titles[i])

