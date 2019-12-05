from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)



# Create your views here.

def login_request(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)


def logout_request(request):
    # print('request', request.POST, request)
    if request.POST.get('logout_current_user'):
        # import pdb; pdb.set_trace()
        logout(request)
        return JsonResponse({'logout': True})
    else:
        return JsonResponse({'logout': 'Error'})