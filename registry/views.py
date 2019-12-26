from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from django.http import HttpResponse
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
    day_count = 1
    for day in generate_days(int(year)):
        print('<============================ day number:', day_count, day, '============================>')
        if day_count == 10:
            print('BREAKING...')
            break
        next_day = day+timedelta(days=1)
        import_url = 'https://ac.naks.ru/auth/external/json.php?url=reestr_personal&popov=Y&from={}&to={}&AUTH_ID=popov@naks.ru'\
            .format(day.strftime('%d.%m.%Y'), next_day.strftime('%d.%m.%Y'))
        import_data_response = json.loads(requests.post(import_url).content.decode('utf8'))
        # print('DAY', day.strftime('%d.%m.%Y'), 'NEXT DAY', next_day.strftime('%d.%m.%Y'))
        for rec in import_data_response:
            print(rec, end="\n")
            adapted_record = RegistryRecordAdapter(rec)
            adapted_record.save_to_db()
            import pdb; pdb.set_trace()
            # import pdb; pdb.set_trace()
        day_count += 1
    if user.is_staff:
        return HttpResponse(
            'starting import records...<br>Year: {}<br>look into console for logging'.format(year)
            )

def personal(request):
    pass