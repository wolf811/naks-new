from django.shortcuts import render
from reestr.models import *
import math

# Create your views here.


def centers(request, direction):
    from .useful import DIRECTIONS
    centers = AccreditedCenter.objects.filter(
        direction=direction, sro_member__status='a').order_by('short_code')
    centers_arr = [c for c in centers]
    directions = DIRECTIONS
    content = {
        "direction": directions[direction],
    }
    if len(centers_arr) > 1:
        middle = math.ceil(len(centers_arr) / 2)
        centers_left = centers_arr[:middle]
        centers_right = centers_arr[middle:]
        content.update({
            "centers_left": centers_left,
            "centers_right": centers_right
        })
    else:
        content.update({
            "centers_left": centers_arr
        })
    # import pdb; pdb.set_trace()
    return render(request, 'reestr/centers.html', content)


def center_details(request):
    pass


