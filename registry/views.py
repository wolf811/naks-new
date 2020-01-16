from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from .models import RegistryRecordPersonal
from .forms import *
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime, timedelta
import requests, json
from registry.utils.registry_import import RegistryRecordAdapter


# Create your views here.
def generate_days(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    d = start_date
    dates = [start_date]
    while d < end_date:
        d += timedelta(days=1)
        dates.append(d)
    return dates

# 'https://ac.naks.ru/auth/external/json.php?url=reestr_personal&popov=Y&from=01.01.2019&to=05.01.2019&AUTH_ID=popov@naks.ru'

@login_required
def initiate_import(request, year):
    user = request.user
    if user.is_staff:
        delete_before = request.GET.get('delete_before')
        break_on = int(request.GET.get('break_on')) if request.GET.get('break_on') else 0
        if delete_before == 'Y':
            RegistryRecordPersonal.objects.all().delete()
        day_count = 1
        for day in generate_days(int(year)):
            print('<============================ day number:', day_count, day, '============================>')
            if break_on > 0 and day_count == break_on:
                print('BREAKING on {}...'.format(break_on))
                break
            next_day = day+timedelta(days=1)
            import_url = 'https://ac.naks.ru/auth/external/json.php?url=reestr_personal&popov=Y&from={}&to={}&AUTH_ID=popov@naks.ru'\
                .format(day.strftime('%d.%m.%Y'), next_day.strftime('%d.%m.%Y'))
            import_data_response = json.loads(requests.post(import_url).content.decode('utf8'))
            # print('DAY', day.strftime('%d.%m.%Y'), 'NEXT DAY', next_day.strftime('%d.%m.%Y'))
            for rec in import_data_response:
                # print(rec, end="\n")
                try:
                    adapted_record = RegistryRecordAdapter(rec)
                    adapted_record.save_to_db()
                except Exception as e:
                    print('!!!------>ERROR import data', e)
                    break
            day_count += 1
        return HttpResponse(
            'starting import records...<br>Year: {}<br>look into console for logging'.format(year)
            )
    else:
        return HttpResponseForbidden('FORBIDDEN')

def personal(request):
    # import pdb; pdb.set_trace()
    print('LEN request', len(request.POST))
    content = {
        'i_am_content': 'true'
    }
    if request.POST.get('search_request'):
        print('REQUEST -------->', request.POST.get('search_request'))
        return render(request, 'registry/includes/registry_table_personal.html', content)
    return render(request, 'registry/registry_main_template.html', content)