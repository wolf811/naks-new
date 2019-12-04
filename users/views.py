from django.shortcuts import render
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm



# Create your views here.

def login_request(request):
    print('request', request)


def logout_request(request):
    # print('request', request.POST, request)
    if request.POST.get('logout_current_user'):
        # import pdb; pdb.set_trace()
        logout(request)
        return JsonResponse({'logout': True})
    else:
        return JsonResponse({'logout': 'Error'})