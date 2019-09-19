from django.shortcuts import render
from reestr.models import *
from django.db.models import Q
import math
from .useful import DIRECTIONS
# Create your views here.


def middle_with_round_array(arr):
    if len(arr) > 1:
        mid = math.ceil(len(arr) / 2)
        arr_left = arr[:mid]
        arr_right = arr[mid:]
        return {"left": arr_left, "right": arr_right}
    else:
        return {"left": arr}


def centers(request, direction):
    active_centers = AccreditedCenter.objects.filter(
        direction=direction, sro_member__status='a', active=True).exclude(
            temporary_suspend_date__isnull=False).order_by('short_code')
    directions = DIRECTIONS
    content = {
        "direction": directions[direction],
    }
    content.update({
        "active_centers": middle_with_round_array(active_centers)
        })
    inactive_by_sro_membership = Q(sro_member__status='na')
    inactive_by_status_of_ac = Q(active=False)
    by_direction = Q(direction=direction)
    by_temporary_suspend_date = Q(temporary_suspend_date__isnull=False)
    inactive_centers = AccreditedCenter.objects.filter(
        inactive_by_sro_membership | inactive_by_status_of_ac
    ).order_by('short_code')
    suspended_centers = AccreditedCenter.objects.filter(
        by_temporary_suspend_date
    ).order_by('short_code')
    content.update({
        "inactive_centers": middle_with_round_array(inactive_centers),
        "suspended_centers": middle_with_round_array(suspended_centers)
    })

    gtu_spr = GTU.objects.all()
    weld_types_spr = WeldType.objects.all()
    levels_spr = Level.objects.all()

    content.update({
        'gtus': gtu_spr,
        'weld_types': weld_types_spr,
        'levels': levels_spr
    })

    return render(request, 'reestr/centers.html', content)


def center_details(request):
    pass


