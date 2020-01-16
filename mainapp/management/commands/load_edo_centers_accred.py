from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.conf import settings
from reestr.models import AccreditedCenter, GTU, WeldType, Level
import requests
import json
import os
import re


def get_edo_auth():
    try:
        if (os.path.join(settings.BASE_DIR, 'secret.json')):
            secret_file = os.path.join(settings.BASE_DIR, 'secret.json')
            with open(secret_file, 'r') as secret_file_:
                secret_data = json.load(secret_file_)
                edo_user = secret_data['edo_user']
                edo_password = secret_data['edo_password']
        return {
            'USER_LOGIN': edo_user,
            'USER_PASSWORD': edo_password,
            'AUTH_FORM': 'Y',
            "TYPE": "AUTH"
        }
    except Exception as e:
        print('EDO AUTH ERROR', e)

head = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--update_center_links', default=False, type=str, help='set starting point')

    def handle(self, *args, **options):
        payload = get_edo_auth()
        personal_centers = [c.short_code for c in AccreditedCenter.objects.filter(direction='personal', active=True)]
        # gtus_bd = [gtu.short_name for gtu in GTU.objects.all() if '(' not in gtu.short_name]
        # gtus_bd_id = [gtu.id for gtu in GTU.objects.all() if '(' not in gtu.short_name]
        # import pdb; pdb.set_trace()
        with requests.Session() as sess:
            login_url = 'https://ac.naks.ru/'
            all_centers_url = 'https://ac.naks.ru/ac/'
            log_me_in = sess.post(login_url, data=payload, headers=head)

            all_centers_page = sess.get(all_centers_url)
            centers_soup = BeautifulSoup(all_centers_page.text, 'html.parser')
            all_centers_links = centers_soup.find_all('a', attrs={"title": "Действия"})
            center_hrefs = []
            for lnk in all_centers_links:
                center_hrefs.append(
                    (lnk.get_text(),
                    'https://ac.naks.ru/ac/{}'.format(lnk.get('href')))
                    )

            if options['update_center_links']:
                for cntr in center_hrefs:
                    if cntr[0] in personal_centers:
                        center = AccreditedCenter.objects.get(short_code=cntr[0])
                        center.center_edo_link = cntr[1]
                        center.save()


            for cntr in center_hrefs:
                if cntr[0] in personal_centers:
                    cntr_page = sess.get(cntr[1])
                    cntr_soup = BeautifulSoup(cntr_page.text, 'html.parser')
                    for tg in cntr_soup.find_all('fieldset'):
                        # load obl_accred
                        if 'Юр.адрес:' in tg.get_text():
                            # print([''.join(i.split()) for i in tg.stripped_strings])
                            # print([''.join(i.split()) for i in tg.stripped_strings])
                            content = [t for t in tg.stripped_strings]
                            print(content)
                            cntr_ur_address = content[1]
                            cntr_city = content[3]
                            cntr_post_address = content[5]
                            cntr_fact_address = content[7]
                            cntr_head = content[9]
                            cntr_org_head = content[11]
                            break
                    # for t in cntr_soup.find_all('span'):
                    #     t_next = t.nextSibling
                    #     if t_next and len(t_next) > 3:
                    #         print('CONTENT', t_next.strip())
                    #         import pdb; pdb.set_trace()
                    phone = cntr_soup.find('span', text=re.compile('Телефон')).nextSibling.strip()
                    fax = cntr_soup.find('span', text=re.compile('Факс')).nextSibling.strip()
                    email = cntr_soup.find('span', text=re.compile('E-mail')).nextSibling.strip()
                    import pdb; pdb.set_trace()
                    break


                        # working
                        # if 'Группы технических устройств' in tg.get_text():
                        #     obl_accred = [''.join(i.split()) for i in tg.stripped_strings]
                        #     # gtus_regex = "['А-Я']{1,5}"
                        #     cntr_gtus = re.findall(r"['А-Я']{1,5}", obl_accred[1])
                        #     cntr_weldtypes = re.findall(r"['А-Я']{1,5}", obl_accred[3])
                        #     cntr_levels = re.findall(r"['A-Z']{1,2}", obl_accred[5])
                        #     center = AccreditedCenter.objects.get(short_code=cntr[0])
                        #     needed_gtus = GTU.objects.filter(short_name__in=cntr_gtus)
                        #     center.gtus.add(*needed_gtus)
                        #     center.save()
                        #     print('CENTER {} SAVED'.format(center), center.gtus.all())



                            # print('GTUS', cntr_gtus, 'WELDTYPES', cntr_weldtypes, 'LEVELS', cntr_levels)

                    # import pdb; pdb.set_trace()


            # tag = soup.span
            # print(soup)
            # for ch in soup.find_all('fieldset'):
            #     if 'Группы технических устройств' in ch.get_text():
            #         # import pdb; pdb.set_trace()
            #         obl_accred = [''.join(i.split()) for i in ch.stripped_strings]
            #         print(obl_accred)