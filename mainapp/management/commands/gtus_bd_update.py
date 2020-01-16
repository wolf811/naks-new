from django.core.management.base import BaseCommand
from reestr.models import GTU, WeldType
from registry.models import RegistryRecordPersonal
import re
import time


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--start_from', default=False, type=int, help='set starting point')
        parser.add_argument('--end', default=False, type=int, help='set end point')
        parser.add_argument('--count', default=False, type=int, help='set records count')


    def handle(self, *args, **options):
        start_from = 0

        if options['start_from']:
            start_from = options['start_from']

        records_count = RegistryRecordPersonal.objects.count()

        if options['count']:
            records_count = start_from+options['count']

        if options['end']:
            records_count = options['end']

        chunk_size = 1000

        # Иванов Евгений Витальевич ['НГДО']
        # ['ГО(1,2,3,4,5,6,7)', 'КО(1,2,3,4,5)', 'ОХНВП(1,2,3,4,15,16)']
        # ['ГО(1,2,2п,3,4,5,6,7)', 'КО(1,2,3,4,5)', 'ОХНВП(1,2,4,9,11,12,13,14,15,16)']
        print('STARTED QUERY', time.ctime())
        bd_gtus = GTU.objects.all().order_by('pk')
        bd_gtus_arr = [gtu.short_name for gtu in bd_gtus]
        bd_gtus_ids = [gtu.id for gtu in bd_gtus]
        bd_gtus_dict = dict(zip(bd_gtus_arr, bd_gtus_ids))
        # import pdb; pdb.set_trace()
        for i in range(start_from, records_count, chunk_size):
            records = RegistryRecordPersonal.objects.all().order_by('pk')[i:i+chunk_size]
            started = time.time()
            for rec in records:
                try:
                    if rec.data['gtus']:
                        rec.data['gtu_ids'] = []
                        if '(' in rec.data['gtus']:
                            rec_groups_tu = re.findall("([А-Я]+?)\((.+?)\)", rec.data['gtus'])
                        else:
                            rec_groups_tu = re.findall("([А-Я]+)", rec.data['gtus'])
                        for group in rec_groups_tu:
                            if type(group) is tuple:
                                for tu_number in group[1].split(','):
                                    rec.data['gtu_ids'].append(bd_gtus_dict['{} ({})'.format(group[0], tu_number)])
                            else:
                                rec.data['gtu_ids'].append(bd_gtus_dict[group])
                        # print('RESULT OF UPDATE:', rec.data['gtus'], rec.data['gtu_ids'])
                        rec.save()
                except Exception as e:
                    print('GTU UPDATE ERROR: ', e, rec.data)
                    continue
            print('---------> i:', i, '<----------- elapsed:', time.time() - started)