from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .forms import CustomUserCreationForm
import requests

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


# Create your views here.

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_request(request):
    # import pdb; pdb.set_trace()
    email = request.data.get("email")
    password = request.data.get("password")
    # edo_token_auth = 'https://ac.naks.ru/auth/external/auth.php?token=74336a72b6314a9dddbbafbcc8155dee51b1'
    # edo_login_url = 'https://ac.naks.ru/auth/external/?LOGIN={}&PASSWORD={}&AUTH_ID=popov@naks.ru'.format(email, password)
    # edo_token = requests.post(edo_login_url)
    # import pdb; pdb.set_trace()
    # print('EDO TOKEN', edo_token.content.decode('utf8'))
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register_request(request):
    email = request.data.get('email')
    password = request.data.get('password')
    ur_status = request.data.get('ur_status')
    print('REGISTER REQUEST', request.data)
    if email is None or password is None or ur_status is None:
        return Response({'error': 'Please provide all registration information'},
        status=HTTP_400_BAD_REQUEST)
    form = CustomUserCreationForm(email=email, password=password)
    if form.is_valid():
        try:
            user, _ = CustomUser.objects.get_or_create(email=email, password=password)
            user.userprofile.status = ur_status
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': '{}'.format(e)})
    else:
        # [(k, v[0].__unicode__()) for k, v in form.errors.items()]
        return Response({'form_error': '{}'.format(form.errors)})



def logout_request(request):
    # print('request', request.POST, request)
    if request.POST.get('logout_current_user'):
        # import pdb; pdb.set_trace()
        logout(request)
        return JsonResponse({'logout': True})
    else:
        return JsonResponse({'logout': 'Error'})