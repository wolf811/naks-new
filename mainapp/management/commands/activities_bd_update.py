from django.core.management.base import BaseCommand
from reestr.models import WeldType, Activity, Level
from registry.models import RegistryRecordPersonal
from reestr.models import AccreditedCenter
import re
import time
from django.db import transaction


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
        db_weldtype = [wt for wt in WeldType.objects.all().order_by('pk')]
        db_activities = [act for act in Activity.objects.all().order_by('pk')]
        db_levels = [lv for lv in Level.objects.all().order_by('pk')]
        join_spr_arr = db_weldtype + db_activities + db_levels
        spr_dict = dict(
            zip(
                [(lambda x: x.short_name if hasattr(x, 'short_name') else x.level)(el) for el in join_spr_arr],
                [el.id for el in join_spr_arr]
                ))
        spr_dict.update({'Руководство': Activity.objects.get(short_name='РиТК').id})
        personal_centers = AccreditedCenter.objects.filter(direction='personal')
        centers_dict = dict(
            zip(
                [c.short_code for c in personal_centers], [c.id for c in personal_centers]
                ))
        for i in range(start_from, records_count, chunk_size):
            records = RegistryRecordPersonal.objects.all().order_by('pk')[i:i+chunk_size]
            with transaction.atomic():
                # updating_records = RegistryRecordPersonal.objects.select_for_update().filter(id__in=records.values_list('id', flat=True))
                updating_records = RegistryRecordPersonal.objects.select_for_update().filter(id__in=records.values_list('id', flat=True))
                started = time.time()
                for rec in updating_records:
                    # try:
                    if rec.data['activity']:
                        # import pdb; pdb.set_trace()
                        rec.data['activity_ids'] = []
                        for act in rec.data['activity'].split(","):
                            if act in spr_dict:
                                rec.data['activity_ids'].append(spr_dict[act])
                            else:
                                new_spr, created = WeldType.objects.get_or_create(short_name=act)
                                rec.data['activity_ids'].append(new_spr.id)
                                if created:
                                    print('NEW SPR CREATED:', new_spr)
                    if rec.data['udost']:
                        rec_lv = rec.data['udost'].split('-')[-2]
                        rec.data['level_id'] = spr_dict[rec_lv]
                        if re.match('[А-Я]', rec.data['udost']):
                            rec.data['udost_center_code_id'] = centers_dict['-'.join(rec.data['udost'].split('-')[0:2])]
                            rec.data['udost_5digit_number'] = rec.data['udost'].split('-')[-1]
                        # rec.data['udost_digit_number']
                    rec.save()
                    # except Exception as e:
                    #     print('RECORD UPDATE ERROR: ', e, rec.data)
                    #     continue
            print('---------> i:', i, '<----------- elapsed:', time.time() - started)