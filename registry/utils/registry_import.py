import json
import datetime
import re
from django.utils.timezone import get_fixed_timezone, utc
from registry.models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404


def date_parse(string):
    date_re = re.compile(
        r'(?P<day>\d{1,2}).(?P<month>\d{1,2}).(?P<year>\d{4})$')
    match = date_re.match(string)
    if match:
        kw = {k: int(v) for k, v in match.groupdict().items()}
        return datetime.date(**kw)


class RegistryRecordAdapter:
    """adapter, that converts data to RegistryRecord model"""

    type_of_import = {
        'personal': RegistryRecordPersonal,
        'materials': RegistryRecordMaterials
    }

    def __init__(self, args):
        self.edo_id = args['id']
        self.fio = args['fio']
        self.title = 'Аттестация {}'.format(self.fio)
        self.company = self.get_or_create_company(args['company'])
        self.active_since = self.converted_date(args['date_create'])
        self.date_created = self.active_since
        self.active_until = self.converted_date(args['active_to'])
        self.extension_date = self.converted_date(args['active_long'])
        self.data = {
            'udost': args['udost'],
            'activity': args['vid_d'],
            'gtus': args['obl_att'],
            'stamp': args['stamp'],
            'position': args['position'],
            'place_of_att': args['place'],
        }

    def converted_date(self, date_string):
        if len(date_string) > 0:
            return datetime.datetime.strptime(date_string, '%d.%m.%Y')
        else:
            return None

    def get_or_create_company(self, company):
        try:
            c = Company.objects.get(name=company)
            return c
        except Company.DoesNotExist:
            c = Company.objects.create(name=company)
            return c

    def save_to_db(self):
        try:
            record_obj = RegistryRecordPersonal.objects.create(**self.__dict__)
            record_obj.save()
        except Exception as e:
            print('ERROR SAVING to DB', e)


class RegistryRecordMapper:
    """relation between RegistryRecords objects and database"""

    def check_if_exist(self, record):
        try:
            Registry.objects.get(title=record.title)
            print('Found')
            return True
        except Exception as e:
            print('Not found')
            return False

    def find_by_id(self, record):
        return get_object_or_404(Registry, pk=record.pk)

    def insert(self, record):
        try:
            record.save()
        except Exception as e:
            print(e)

    def update(self, id, **params):
        try:
            record = Registry.objects.get(pk=id)
            record.save(params)
        except Exception as e:
            print(e)

    def delete(self, record):
        try:
            rec = Registry.objects.get(pk=record.pk)
            rec.delete()
        except Exception as e:
            print(e)


class Importer:
    """importer, converter to json, and loader to database
        with checking if already loaded"""
    type_of_import = {
        'personal': RegistryRecordPersonal,
        'materials': RegistryRecordMaterials
    }
    #  https://ac.naks.ru/auth/external/json.php
    # url=reestr_personal&popov=Y&from=01.01.2019&to=05.01.2019&AUTH_ID=popov@naks.ru

    def __init__(self, url):
        self.data = self.get_data_from_url(url)
        self.mapper = RegistryRecordMapper()

    def get_data_from_url(self, url):
        data = urllib.request.urlopen(url)
        read_data = data.read()
        json_data = json.loads(read_data.decode('utf8'))
        return json_data

    def check_if_already_loaded(self, record):
        pass

    def save_data_to_db(self, record):
        """save every data record to DB using RegistryRecordAdapter"""
        args = {
            'date_created': record['date_create'],
            'title': record['fio']+'-'+record['vid_d']+'-'+record['stamp']+'-'+record['date_create'],
            'org': record['company'],
            'typeof': 'Аттестация персонала',
            'params': json.dumps(record),
            'status': 0
        }
        adapted_record = RegistryRecordAdapter(args)
        print(adapted_record.__dict__)
        record = Registry(**adapted_record.__dict__)
        if self.mapper.check_if_exist(record):
            """check if record already there"""
            print('Already there', record.title)
        else:
            """if not - insert with mapper method"""
            self.mapper.insert(record)
            print('SAVED NEW RECORD', record.title)
