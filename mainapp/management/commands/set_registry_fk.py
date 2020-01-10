from django.core.management.base import BaseCommand
from reestr.models import AccreditedCenter, AccreditedCertificationPoint, SROMember
from registry.models import RegistryRecordPersonal
import re
import time


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--start_from', default=False, type=int, help='set starting point')


    def handle(self, *args, **options):
        start_from = 0
        if options['start_from']:
            start_from = options['start_from']

        records_count = RegistryRecordPersonal.objects.count()
        # records_count = 2000
        chunk_size = 1000
        ap_template = ', \d{1,2}АП'
        regex = re.compile(ap_template)
        inactive_sro_member = SROMember.objects.filter(status='na').first()
        for i in range(start_from, records_count, chunk_size):
            records = RegistryRecordPersonal.objects.all().order_by('pk')[i:i+chunk_size]
            started = time.time()
            for rec in records:
                if rec.data['place_of_att']:
                    code = rec.data['place_of_att'].strip()
                    if 'АП' in code:
                        match = re.search(regex, code)
                        start_end = match.span()
                        point = code[start_end[0]:start_end[1]]
                        center_code = code.replace(point, "")
                        center, center_created = AccreditedCenter.objects.get_or_create(
                            short_code=center_code,
                            direction='personal')
                        cert_point_code = point.replace(", ", "")
                        cert_point, cert_point_created = AccreditedCertificationPoint.objects.get_or_create(
                            short_code=cert_point_code,
                            parent=center
                        )
                        rec.data['center_pk'] = center.pk
                        rec.data['cert_point_pk'] = cert_point.pk
                    else:
                        center, created = AccreditedCenter.objects.get_or_create(short_code=code)
                        rec.data['center_pk'] = center.pk
                    rec.save()
            print('---------> i:', i, '<----------- elapsed:', time.time() - started)







