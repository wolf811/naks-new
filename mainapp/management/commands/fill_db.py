from django.core.management.base import BaseCommand
from django.core.files import File
from mixer.backend.django import mixer
from mainapp.models import *
import random, os

for r, d, f in os.walk(os.path.join(os.getcwd(), 'media')):
    for file in f:
        if file.startswith(('img', 'document', 'file')) and len(file) > 13:
            print('removed trash: ', file)
            os.remove(os.path.join(r, file))

news_titles = [
    'Конференция НАКС',
    'Общее собрание',
    'Семинар НАКС',
    'Съезд НАКС',
    'Съезд НАКС',
    'Открытие центра',
    'Заключение соглашения',
    'Заключение соглашения',
]

categories = [
    'Общее',
    'СРО',
    'САСв',
    'СПКС',
    'События и мероприятия',
    'ТК364',
]

tags = [
    'Общее',
    'СРО',
    'САСв',
]

pictures = [
    'media/img_1.jpg',
    'media/img_2.jpg',
    # 'media/img_3.png',
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Post.objects.all().delete()
        Category.objects.all().delete()
        Contact.objects.all().delete()
        ContactSubdivision.objects.all().delete()
        Document.objects.all().delete()

        mixer.cycle(10).blend(
            Document,
            # title=mixer.sequence('document_naks_{0}'),
            main_page_rotation=True,
        )

        mixer.cycle(10).blend(ContactSubdivision, title=mixer.sequence('subdivision_{0}'))
        mixer.cycle(20).blend(
            Contact,
            description=mixer.RANDOM,
            subdivision=mixer.SELECT,
            phone=mixer.RANDOM,
            phone_secondary=mixer.RANDOM,
            email=mixer.RANDOM,
            number=mixer.RANDOM
            )

        for i in range(len(tags)):
            mixer.blend(Tag, name=tags[i])

        for i in range(len(categories)):
            mixer.blend(Category, name=categories[i])

        for i in range(len(news_titles)):
            mixer.blend(
                Post,
                title=news_titles[i],
                active=True if random.randint(0, 100) > 20 else False,
                mark_as_announcement=True if random.randint(0, 100) > 60 else False,
                category=random.choice([category for category in Category.objects.all()]),
                subtitle=mixer.RANDOM,
                short_description=mixer.RANDOM,
                full_description=mixer.RANDOM,
                main_picture=File(open(random.choice(pictures), 'rb')),
            )
            print('creating posts:', news_titles[i])
