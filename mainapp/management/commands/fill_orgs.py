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

        for i in range(5):
            mixer.blend(
                SROMember,
                chief=random.choice(org_chiefs),
                short_name=random.choice(org_short_titles)
            )
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
            mixer.blend(AccreditedCenter, sro_member=member)

        for lv in levels:
            Level.objects.create(level=lv)

        for accred_center in AccreditedCenter.objects.all():
            accred_center.gtus.add(*[gtu for gtu in GTU.objects.all()])
            accred_center.weldtypes.add(*[weld for weld in WeldType.objects.all()])
            accred_center.levels.add(*[level for level in Level.objects.all()])
            accred_center.member = random.choice(
                [member for member in SROMember.objects.all()]
                )

        print('orgs creation complete')
