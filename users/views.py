from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.core.mail import send_mail
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

def _get_absolute_url(request, relative_url):
    return "{0}://{1}{2}".format(
        request.scheme,
        request.get_host(),
        relative_url
    )


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
    # import pdb; pdb.set_trace()
    if not user:
        return Response({'errors': 'Данные для авторизации не верны'})
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
    honeypot = request.data.get('honeypot')
    print('REGISTER REQUEST', request.data)
    if honeypot:
        return Response({
            'failure': 'input is incorrect'
        }, status=HTTP_400_BAD_REQUEST)
    if email is None or password is None or ur_status is None:
        return Response(
            {'error': 'Please provide all registration information'},
            status=HTTP_400_BAD_REQUEST)
    form_data = {
        'email': email,
        'password1': password,
        'password2': password
    }
    form = CustomUserCreationForm(form_data)
    if form.is_valid():
        try:
            # user, created = CustomUser.objects.get_or_create(email=email, password=password)
            user = form.save()
            user.userprofile.status = ur_status
            user.save()
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': '{}'.format(e)})
    else:
        errors = [(k, v[0]) for k, v in form.errors.items()]
        return Response({'form_error': errors})


def logout_request(request):
    # print('request', request.POST, request)
    if request.POST.get('logout_current_user'):
        # import pdb; pdb.set_trace()
        logout(request)
        return JsonResponse({'logout': True})
    else:
        return JsonResponse({'logout': 'Error'})

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def recover_password_request(request):
    email = request.data.get('email')
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        try:
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
            # token for password reset
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # import pdb; pdb.set_trace()
            update_password_url = reverse(
                'users:update-password', kwargs={'uid': uid.decode(), 'token': token}
            )
            send_mail(
                'Password reset',
                'Password reset url: {}'.format(_get_absolute_url(request, update_password_url)),
                'noreply@naks.ru',
                [email],
                fail_silently=False,
            )
            return Response({'password_recovery_email_sent': email})
        except CustomUser.DoesNotExist:
            return Response({'user_does_not_exist': email})

    else:
        errors = [(k, v[0]) for k, v in form.errors.items()]
        return Response({'password_recovery_error': errors}, status=HTTP_200_OK)

def validate_signed_token(uid, token, require_token=True):
    """
    Validates a signed token and uid and returns the user who owns it.
    :param uid: The uid of the request
    :param token: The signed token of the request if one exists
    :param require_token: Whether or not there is a signed token, the token parameter is ignored if False
    :return: The user who's token it is, if one exists, None otherwise
    """
    # user_model = get_user_model()
    user_model = CustomUser
    try:
        # import pdb; pdb.set_trace()
        uid = force_text(urlsafe_base64_decode(uid))
        user = user_model.objects.get(pk=uid)
        if require_token:
            if user is not None and default_token_generator.check_token(user, token):
                return user
        else:
            return user
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist) as e:
        print('token not validated error', e)
        pass
    return None


def update_password(request, uid, token):
    user = validate_signed_token(uid, token)
    if not user:
        return HttpResponseForbidden()  # Just straight up forbid this request, looking fishy already!
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        form = SetPasswordForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            Token.objects.filter(user_id__exact=user.pk).delete()
            # return redirect(reverse('mhacks-login') + '?username=' + user.email)
            return JsonResponse({'password_updated': 'successfully'})
        else:
            errors = [v for k, v in form.errors.items()]
            return JsonResponse({'form_errors': errors})
    return render(request, 'users/password_change.html', {
        'user': user,
        'uid': uid,
        'token': token,
        })