from django.shortcuts import render
from reestr.models import *

# Create your views here.


def centers(request, direction):
    centers = AccreditedCenter.objects.filter(
        direction=direction, sro_member__status='a').order_by('short_code')
    centers_arr = [c for c in centers]
    content = {}
    centers_left = []
    centers_right = []
    if len(centers_arr) > 1:
        if len(centers_arr) % 2 != 0:
            for i in range(0, len(centers_arr)/2):
                centers_left.append(centers_arr[i])
        else:
            pass
    else:
        content.update({'centers_left': centers_arr})
    return render(request, 'reestr/centers.html', content)


def center_details(request):
    pass


