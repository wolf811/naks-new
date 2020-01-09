from django.core.management.base import BaseCommand
from reestr.models import AccreditedCenter, AccreditedCertificationPoint
from reestr.models import SROMember
import os


def load_centers_personal():
    org_names_and_centers = []
    centers_file_name = 'centers_personal.csv'
    if (os.path.join(os.getcwd(), centers_file_name)):
        # print('file is here', os.path.join(os.getcwd(), centers_file_name))
        centers_file = os.path.join(os.getcwd(), centers_file_name)
        with open(centers_file, 'rb') as f:
            lines = f.readlines()
            for line in lines:
                center_line = line.decode('utf8').rstrip().split(';')
                org_name = center_line[0]
                center_code = center_line[1]
                org_names_and_centers.append((org_name, center_code))
        # print('---->>>> org_names_and_addresses loaded')
        return org_names_and_centers
    else:
        return []


class Command(BaseCommand):
    def handle(self, *args, **options):
        centers = load_centers_personal()
        for center in centers:
            if SROMember.objects.filter(full_name=center[0]).exists():
                org_name = center[0]
                center_code = center[1]
                org = SROMember.objects.get(full_name=org_name)
                org.short_name = org_name
                if AccreditedCenter.objects.filter(sro_member=org, direction='personal').exists():
                    print('center exists, deleting...')
                    print('creating new center...')
                    old_personal_centers = AccreditedCenter.objects.filter(sro_member=org, direction='personal')
                    old_personal_centers.delete()
                    matching_codes = AccreditedCenter.objects.filter(short_code=center_code)
                    matching_codes.delete()
                    new_center = AccreditedCenter.objects.create(
                        short_code=center_code,
                        sro_member=org,
                        direction='personal')
                    print('new center created, FK link created', new_center)
            else:
                print('NONE, creating...')
                new_org = SROMember.objects.create(full_name=center[0], short_name=center[0])
                print('created new org', new_org.full_name)