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
    'ТОР-1ГАЦ',
    'ЗУР-1ГАЦ',
]

csp_short_codes = [
    'БР-1ЦСП',
    'ТОР-1ЦСП',
    'ЗУР-2ЦСП',
    'МР-7ЦСП',
    'ЦР-5ЦСП',
    'СУР-3ЦСП',
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
    ('АПС', 'Автоматическая сварка самозащитной порошковой проволокой'),
    ('АФ', 'Автоматическая сварка под флюсом'),
    ('АФЛН', 'Автоматическая наплавка ленточным электродом под флюсом'),
    ('АФПН', 'Автоматическая наплавка проволочным электродом под флюсом'),
    ('ВЧС', 'Высокочастотная сварка'),
]

attsm_types = [
    ('Гз', 'Газы защитные'),
    ('Гг', 'Газы горючие'),
    ('Пп', 'Проволока порошковая'),
    ('Пс', 'Проволока сплошного сечения'),
]

attso_types = [
    ('A', 'Оборудование для дуговой сварки (наплавки)'),
    ('B', 'Оборудование для газовой сварки'),
    ('C', 'Газы защитные'),
    ('D', 'Оборудование для контактной сварки'),
    ('E', 'Оборудование для высокочастотной и индукционной сварки (наплавки)'),
    ('F', 'Оборудование для высокочастотной и индукционной сварки (наплавки)'),
    ('G', 'Оборудование для высокочастотной и индукционной сварки (наплавки)'),
]

levels = ['I', 'II', 'III', 'IV']


gtus = [
    ('ГДО', 'Горнодобывающее оборудование'),
    ('КО', 'Котельное оборудование'),
    ('НГДО', 'Нефтегазодобывающее оборудование'),
    ('ОТОГ', 'Оборудование для транспортировки опасных грузов'),
    ('ПТО', 'Подъемно-транспортное оборудование'),
]

tus = [
    'Технические устройства для горнодобывающих и горно-обогатительных производств и подземных объектов',
    'Трубопроводы систем внутреннего газоснабжения',
    'Наружные газопроводы низкого, среднего и высокого давления стальные',
    'Паровые котлы с давлением пара более 0,07 МПа и водогрейные котлы с температурой воды выше 115°С',
    'Арматура и предохранительные устройства',
    'Металлические конструкции пролётных строений, опор и пилонов стальных мостов при изготовлении в заводских условиях',
    'Технологическое оборудование и трубопроводы для черной и цветной металлургии',
    'Промысловые и магистральные нефтепродуктопроводы, трубопроводы нефтеперекачивающих станций (НПС), обеспечивающие транспорт нефти и нефтепродуктов при сооружении, реконструкции и капитальном ремонте',
    'Промысловые и магистральные газопроводы и конденсатопроводы; трубопроводы для транспортировки товарной продукции, импульсного, топливного и пускового газа в пределах: установок комплексной подготовки газа (УКПГ), компрессорных станций (КС), дожимных компрессорных станций (ДКС), станций подземного хранения газа (СПХГ), газораспределительных станций (ГРС), узлов замера расхода газа (УЗРГ) и пунктов редуцирования газа (ПРГ)',
    'Цистерны',
    'Оборудование химических, нефтехимических, нефтеперерабатывающих производств, работающее под вакуумом',
    'Центрифуги, сепараторы',
    'Подъемники (вышки)',
]

activities = [
    ('РиТК', 'Руководство и технический контроль за проведением сварочных работ'),
    ('ПиА', 'Участие в работе органов по подготовке и аттестации')
]


qual_list = [
    {
        'full_name': 'Сварщик',
        'short_name': '40.002',
        'qualifications': [
            'Сварщик дуговой сварки плавящимся покрытым электродом (2 уровень квалификации)',
            'Сварщик дуговой сварки плавящимся покрытым электродом (3 уровень квалификации)',
            'Сварщик дуговой сварки плавящимся покрытым электродом (4 уровень квалификации)',
            'Сварщик дуговой сварки самозащитной проволокой (2 уровень квалификации)',
            'Сварщик дуговой сварки самозащитной проволокой (3 уровень квалификации)',
            'Сварщик дуговой сварки самозащитной проволокой (4 уровень квалификации)',
            'Сварщик дуговой сварки плавящимся электродом в защитном газе (2 уровень квалификации)',
        ]
    },
    {
        'full_name': 'Резчик термической резки металлов',
        'short_name': '40.109',
        'qualifications': [
            'Резчик ручной кислородной резки (2 уровень квалификации)',
            'Резчик ручной кислородной резки (3 уровень квалификации)',
        ]
    },
    {
        'full_name': 'Контролер сварочных работ',
        'short_name': '40.114',
        'qualifications': [
            'Контролер подготовительных и сборочных работ в сварочном производстве (4 уровень квалификации)',
            'Контролер сварочных работ (4 уровень квалификации)',
            'Контролер технического контроля сварочного производства (5 уровень квалификации)',
            'Контролер технического контроля сварных конструкций (5 уровень квалификации)',
        ]
    },
]



class Command(BaseCommand):
    def handle(self, *args, **options):
        SROMember.objects.all().delete()
        SO.objects.all().delete()
        GTU.objects.all().delete()
        Qualification.objects.all().delete()
        WeldType.objects.all().delete()
        Activity.objects.all().delete()
        Level.objects.all().delete()
        AccreditedCenter.objects.all().delete()
        City.objects.all().delete()

        if City.objects.count() == 0:
            for i in range(30):
                City.objects.create(title=random.choice(city_titles))

        if SROMember.objects.count() == 0:
            for i in range(100):
                mixer.blend(
                    SROMember,
                    chief=random.choice(org_chiefs),
                    short_name=random.choice(org_short_titles),
                    status=lambda: 'a' if random.randint(0, 100) < 80 else 'na'
                )
        print('sro orgs created')
        for member in SROMember.objects.all():
            member.city = City.objects.order_by("?").first()
            member.save()
        print('cities set ready')
        if WeldType.objects.count() == 0:
            for weld in weld_types:
                mixer.blend(
                    WeldType,
                    short_name=weld[0],
                    full_name=weld[1]
                )
        print('weld set ready')
        for gtu in gtus:
            gtu_ = mixer.blend(
                GTU,
                short_name=gtu[0],
                full_name=gtu[1],
            )
            for tu in tus[:random.randint(0, len(tus))]:
                mixer.blend(
                    GTU,
                    short_name="{} ({})".format(gtu[0], tus.index(tu)+1),
                    full_name=tu,
                    parent=gtu_
                )
        if SM.objects.count() == 0:
            for sm in attsm_types:
                mixer.blend(
                    SM,
                    short_name=sm[0],
                    full_name=sm[1]
                )
        if SO.objects.count() == 0:
            for so in attso_types:
                so_ = mixer.blend(
                    SO,
                    short_name=so[0],
                    full_name=so[1]
                )
                for so_subtype in attso_types[:random.randint(0, len(attso_types))]:
                    mixer.blend(
                        SO,
                        short_name="{}{}".format(so[0], attso_types.index(so_subtype)+1),
                        full_name=so_subtype[1],
                        parent=so_
                    )
        if Activity.objects.count() == 0:
            for act in activities:
                mixer.blend(
                    Activity,
                    short_name=act[0],
                    full_name=act[1]
                )

        for el in qual_list:
            ps = mixer.blend(Qualification, short_name=el['short_name'], full_name=el['full_name'], parent=None)
            for qual in el['qualifications']:
                pk = mixer.blend(
                    Qualification,
                    short_name='{}_{}'.format(ps.short_name, el['qualifications'].index(qual)+1),
                    full_name=qual,
                    parent=ps)

        print('all spr set ready')
        center_count = 0
        for member in SROMember.objects.all():
            mixer.blend(
                AccreditedCenter,
                sro_member=member,
                short_code=random.choice(short_codes),
                active=lambda: True if random.randint(0, 100) < 80 else False,
                temporary_suspend_date=mixer.RANDOM if random.randint(0, 100) > 95 else None,
                direction='personal'
                )
            if random.randint(0, 100) < 70:
                mixer.blend(
                    AccreditedCenter,
                    sro_member=member,
                    short_code=random.choice(csp_short_codes),
                    active=lambda: True if random.randint(0, 100) < 80 else False,
                    temporary_suspend_date=mixer.RANDOM if random.randint(0, 100) > 95 else None,
                    direction='specpod'
                    )
            if random.randint(0, 100) < 50:
                acsm_center = mixer.blend(
                    AccreditedCenter,
                    sro_member=member,
                    short_code=lambda: 'АЦСМ-{}'.format(center_count),
                    active=lambda: True if random.randint(0, 100) < 80 else False,
                    temporary_suspend_date=mixer.RANDOM if random.randint(0, 100) > 95 else None,
                    direction='attsm'
                )
            if random.randint(0, 100) < 70:
                acso_center = mixer.blend(
                    AccreditedCenter,
                    sro_member=member,
                    short_code=lambda: 'АЦСО-{}'.format(center_count),
                    active=lambda: True if random.randint(0, 100) < 80 else False,
                    temporary_suspend_date=mixer.RANDOM if random.randint(0, 100) > 95 else None,
                    direction='attso'
                )
            if random.randint(0, 100) < 80:
                acst_center = mixer.blend(
                    AccreditedCenter,
                    sro_member=member,
                    short_code=lambda: 'АЦСТ-{}'.format(center_count),
                    active=lambda: True if random.randint(0, 100) < 80 else False,
                    temporary_suspend_date=mixer.RANDOM if random.randint(0, 100) > 95 else None,
                    direction='attst'
                )
            if random.randint(0, 100) < 50:
                cok = mixer.blend(
                    AccreditedCenter,
                    sro_member=member,
                    short_code=lambda: 'ЦОК-0{}'.format(center_count),
                    active=True,
                    direction='qualifications',
                    cok_nark_code="77.0{}".format(center_count)
                )
            center_count += 1


        # for acsm in acsm_centers:
        #     acsm.direction = 'attsm'
        #     acsm.save()
        # print('centers created')

        for lv in levels:
            Level.objects.create(level=lv)
        print('levels created')
        all_gtu = [gtu for gtu in GTU.objects.all()]
        all_weldtypes = [weld for weld in WeldType.objects.all()]
        all_levels = [level for level in Level.objects.all()]
        all_so_types = [so for so in SO.objects.all()]
        all_sm_types = [sm for sm in SM.objects.all()]

        for accred_center in AccreditedCenter.objects.filter(
                active=True, temporary_suspend_date__isnull=True):
            print('fillig obl_d: {}'.format(accred_center.short_code))
            if accred_center.direction != 'qualifications':
                accred_center.gtus.add(*all_gtu)
            if accred_center.direction == 'attsm':
                accred_center.sm_types.add(*all_sm_types)
            if accred_center.direction in ['personal', 'attst']:
                accred_center.weldtypes.add(*all_weldtypes)
            if accred_center.direction in ['personal', 'specpod']:
                accred_center.levels.add(*all_levels)
                if random.randint(0, 100) > 80:
                    accred_center.activities.add(*[act for act in Activity.objects.all()])
            if accred_center.direction == 'attso':
                accred_center.so_types.add(*all_so_types)
            dice = random.randint(0, 100)
            if dice > 70:
                accred_center.special_tn = True
            another_dice = random.randint(0, 100)
            if another_dice > 80:
                accred_center.special_gp = True
            if accred_center.direction == 'qualifications':
                accred_center.qualifications.add(*[qual for qual in Qualification.objects.all()])

            accred_center.save()

        print('orgs creation complete')
