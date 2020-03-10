import operator
from functools import reduce
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from users.models import CustomUser
from .models import RegistryRecordPersonal
from reestr.models import AccreditedCertificationPoint, AccreditedCenter
from .forms import *
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from datetime import datetime, timedelta
import requests, json
from registry.utils.registry_import import RegistryRecordAdapter
from django.db.models import Q
from django.core.paginator import Paginator

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
    """ import several numbers of records """
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
    """main view for reestr personal page with searching and pagination"""
    # import pdb; pdb.set_trace()
    content = {
        'i_am_content': 'true'
    }
    if request.POST.get('search_request'):
        print('REQUEST -------->', request.POST)

        # import pdb; pdb.set_trace()
        # start filling query list to use and_ operator
        query_list = []

        queries_factory = {
            "certcenter_query": Q(
                data__center_pk=int(request.POST.get(
                'certcenter_query'))) if request.POST.get('certcenter_query') else None,
            "certpoint_query": Q(
                data__cert_point_pk=AccreditedCertificationPoint.objects.filter(
                parent__id=request.POST.get("certcenter_query"),
                short_code=request.POST.get("certpoint_query")).first().pk) if all(
                    [request.POST.get("certpoint_query"), request.POST.get(
                        "certcenter_query")]) else None,
            "fio_query": Q(
                fio__istartswith=request.POST.get(
                'fio_query')) if request.POST.get("fio_query") else None,
            "company_query": Q(
                company__name__icontains=request.POST.get(
                'company_query')) if request.POST.get("company_query") else None,
            "stamp_query": Q(
                data__stamp=request.POST.get(
                'stamp_query')) if request.POST.get("stamp_query") else None,
            "udost_center_code_query": Q(
                data__udost_center_code_id=int(request.POST.get("udost_center_code_query"))) if request.POST.get(
                    "udost_center_code_query") else None,
            "udost_level_query": Q(
                data__level_id=int(request.POST.get("udost_level_query"))) if request.POST.get(
                    "udost_level_query") else None,
            "udost_five_digit_number_query": Q(
                data__udost_5digit_number=request.POST.get(
                    "udost_five_digit_number_query")) if request.POST.get(
                        "udost_five_digit_number_query") else None,
            "active_since_start_query": Q(
                active_since__gte=datetime.date(request.POST.get("active_since_start_query"))) if \
                request.POST.get("active_since_start_query") else None
        }

        # import pdb; pdb.set_trace()

        for req in request.POST:
            if req.endswith('_query'):
                query_list.append(queries_factory[req])

        if not query_list:
            query_list.append(Q(pk__isnull=False))

        query = reduce(operator.and_, query_list)
        count = RegistryRecordPersonal.objects.filter(query).count()
        if count < 500:
            records_list = RegistryRecordPersonal.objects.filter(query).order_by('-active_since')
            print("---->", records_list.explain())
            print("---->", records_list.query)
            paginator = Paginator(records_list, 25) # show 25 per page
            page = request.POST.get('page')
            records = paginator.get_page(page)
            content.update({
                "search_result_count": count,
                "records": records
                })
            return render(request, 'registry/includes/registry_table_personal.html', content)
        return JsonResponse({"specify_request_error": "Слишком много результатов поиска, уточните запрос: {}".format(count)})
    return render(request, 'registry/registry_main_template.html', content)
