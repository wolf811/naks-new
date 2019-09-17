from django.core.management.base import BaseCommand
# from django.core.files import File
from mixer.backend.django import mixer
from reestr.models import *
import random, os


org_short_titles = [
    'ООО АСЦ Сварка СтройТЭК',
    'ООО Аттестационный Центр Городского Хозяйства',
    'ООО Аттестационный центр Калужской области',
    'ООО АЦ НАКС-Ямал',
    'ООО ГАЦ ВВР',
]

short_codes = [
    'БР-1ГАЦ',
    'ЗУР-1ГАЦ',
    'СЗР-1ГАЦ',
    'МУР-1ГАЦ',
    'БОР-1ГАЦ',
    'ФУР-1ГАЦ',
    'ПУК-1ГАЦ',
]

city_titles = [
    'Нижний новгород',
    'Санкт-Петербург',
    'Петропавловск-Камчатский',
    'Сочи',
    'Самара',
    'Казань',
    'Архангельск',
    'Москва',
    'Магадан',
    'Петропавловск-Камчатский Архангельский'
]


org_chiefs = [
    'Щеголев Игорь Львович',
    'Фокин Георгий Анатольевич',
    'Радченко Михаил Васильевич',
    'Нестеренко Нина Афанасьевна',
    'Советченко Борис Федорович',
]


weld_types = [
    ('АПГ', 'Автоматическая сварка плавящимся электродом в среде активных газов и смесях'),
    ('Г', 'Газовая сварка'),
    ('АФ', 'Автоматическая сварка под флюсом'),
    ('МАДП', 'Механизированная аргонодуговая сварка плавящимся электродом'),
    ('НИ', 'Сварка нагретым инструментом'),
]


levels = ['I', 'II', 'III', 'IV']


gtus = [
    ('ГДО', 'Горнодобывающее оборудование'),
    ('КО', 'Котельное оборудование'),
    ('НГДО', 'Нефтегазодобывающее оборудование'),
    ('ОТОГ', 'Оборудование для транспортировки опасных грузов'),
    ('ПТО', 'Подъемно-транспортное оборудование'),
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        SROMember.objects.all().delete()
        SO.objects.all().delete()
        GTU.objects.all().delete()
        WeldType.objects.all().delete()
        Level.objects.all().delete()
        AccreditedCenter.objects.all().delete()
        City.objects.all().delete()

        for i in range(30):
            City.objects.create(title=random.choice(city_titles))

        for i in range(105):
            mixer.blend(
                SROMember,
                chief=random.choice(org_chiefs)
            )
        for member in SROMember.objects.all():
            member.city = City.objects.order_by("?").first()
            member.save()
        for weld in weld_types:
            mixer.blend(
                WeldType,
                short_name=weld[0],
                full_name=weld[1]
            )
        for gtu in gtus:
            mixer.blend(
                GTU,
                short_name=gtu[0],
                full_name=gtu[1]
            )
        for member in SROMember.objects.all():
            mixer.blend(
                AccreditedCenter,
                sro_member=member,
                short_code=random.choice(short_codes)
                )

        for lv in levels:
            Level.objects.create(level=lv)

        for accred_center in AccreditedCenter.objects.all():
            accred_center.gtus.add(*[gtu for gtu in GTU.objects.all()])
            accred_center.weldtypes.add(*[weld for weld in WeldType.objects.all()])
            accred_center.levels.add(*[level for level in Level.objects.all()])
            accred_center.direction = 'personal'
            dice = random.randint(0, 100)
            if dice > 70:
                accred_center.special = 'tn'
            accred_center.save()
            # accred_center.member = random.choice(
            #     [member for member in SROMember.objects.all()]
            #     )

        print('orgs creation complete')
