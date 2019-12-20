from django.shortcuts import render
from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, EdoUser
from .forms import CustomUserCreationForm, EdoUserCreationForm
from smtplib import SMTPException
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from django.template.loader import get_template
from django.shortcuts import redirect
import datetime
import requests
from django.utils import timezone



# from django.template import Context
# from django.core.mail import EmailMultiAlternatives

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
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    # edo_token_auth = 'https://ac.naks.ru/auth/external/auth.php?token='
    if '@' not in email:
        # import pdb; pdb.set_trace()
        identifier = email

        edo_login_data = {
            'LOGIN': identifier,
            'PASSWORD': password,
            'AUTH_ID': 'popov@naks.ru' #TODO: must be in settings with token
        }

        try:
            edo_user = EdoUser.objects.get(identifier=identifier)
            edo_token = edo_user.userprofile.edo_token
            refresh_token = edo_user.userprofile.edo_refresh_token
            token, _ = Token.objects.get_or_create(user=edo_user)
            token_created = edo_user.userprofile.edo_token_created
            one_hour_ago = (timezone.now() - datetime.timedelta(hours=1))
            #TODO: дополнительная проверка можно ли сравнивать пустое поле с час назад
            # import pdb; pdb.set_trace()
            if token_created > one_hour_ago:
                print('TOKEN IS FRESH, logging in...', edo_token, 'created', token_created, '1h ago:', one_hour_ago)
                login(request, edo_user)
                return Response({
                    'token': token.key,
                    'edo_token': edo_token,
                    'edo_token_created': token_created.isoformat()
                })
            else:
                print('REFRESHING TOKEN:', edo_token, 'created', token_created, '1h ago:', one_hour_ago)
                refresh_token_url = 'https://ac.naks.ru/auth/external/check.php?token={}&refresh={}&AUTH_ID=popov@naks.ru'\
                        .format(
                            edo_token, refresh_token
                        )
                print('REFRESH URL:', refresh_token_url)
                refresh_data = {
                    'token': edo_token,
                    'refresh': refresh_token,
                    'AUTH_ID': 'popov@naks.ru' #TODO:
                }
                fresh_token = requests.post(refresh_token_url).content.decode('utf8')
                new_edo_refresh_token, new_edo_token = tuple(fresh_token.split("."))
                edo_user.userprofile.edo_token = new_edo_token
                edo_user.userprofile.edo_refresh_token = new_edo_refresh_token
                edo_user.userprofile.edo_token_created = timezone.now()

                edo_user.save()
                login(request, edo_user)
                return Response({
                    'edo_token': new_edo_token,
                    'token': token.key,
                    'edo_token_created': timezone.now().isoformat()
                })
            # print('TOKEN', edo_token, 'REFRESH TOKEN', refresh_token, 'TOKEN CREATED', token_created)
            user = authenticate(email=identifier, password=password)
            if not user:
                return Response({'error': 'Данные для авторизации не верны'})
            login(request, user)
            return Response({'token': token.key, 'edo_token': edo_token})

        except EdoUser.DoesNotExist:
                print('EDO USER DOES NOT EXIST, creating edo user')
                #check if edo has this user
                edo_login_url = 'https://ac.naks.ru/auth/external/'
                edo_token_string = requests.post(edo_login_url, data=edo_login_data)\
                    .content.decode('utf8')
                edo_refresh_token, edo_token = tuple(edo_token_string.split("."))
                if len(edo_token_string) > 0:
                    edo_user = EdoUser.objects.create_user(
                        email=identifier,
                        identifier=identifier,
                        password=password)
                    # import pdb; pdb.set_trace()
                    edo_user.userprofile.edo_token = edo_token
                    edo_user.userprofile.edo_refresh_token = edo_refresh_token
                    edo_user.save()
                    token, _ = Token.objects.get_or_create(user=edo_user)
                    print('EDO USER CREATED', edo_user)
                    login(request, edo_user)
                    return Response({
                        'token': token.key,
                        'edo_token': edo_token,
                        'edo_token_created': timezone.now().isoformat()
                        })
                    # edo_login_url = 'https://ac.naks.ru/auth/external/?LOGIN={}&PASSWORD={}&AUTH_ID=popov@naks.ru'.format(email, password)
                    # edo_token_refresh_url = 'https://ac.naks.ru/auth/external/check.php?token=74336a72b6314a9dddbbafbcc8155dee51b1&refresh=9a47d78fe5979337'
                    # token, _ = Token.objects.get_or_create(user=edo_user)
                else:
                    return Response({'errors', 'Данные для авторизации не верны'})

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
        errors = [{'field': k, 'errors': v} for k, v in form.errors.items()]
        # import pdb; pdb.set_trace()
        return Response({'form_errors': errors})


def logout_request(request):
    # print('request', request.POST, request)
    if request.POST.get('logout_current_user'):
        # import pdb; pdb.set_trace()
        logout(request)
        return JsonResponse({'logout': True})
    else:
        logout(request)
        return redirect('index')

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
            plaintext_message = get_template('users/email_plain.txt')
            html_message = get_template('users/email_template.html')

            cntxt = {
                'username': user,
                'password_change_link': _get_absolute_url(request, update_password_url)
                }

            subject, from_email, to = 'НАКС: восстановление пароля учетной записи', 'noreply@naks.ru', email
            text_content = plaintext_message.render(cntxt)
            html_content = html_message.render(cntxt)
            # Ссылка для восстановления пароля на сайте НАКС (naks.ru):
            # _get_absolute_url(request, update_password_url)
            send_mail(
                subject,
                text_content,
                from_email,
                [to],
                fail_silently=False,
                html_message=html_content
            )
            return Response({
                'password_recovery_email_sent':
                'На указанный адрес отправлено письмо со \
                ссылкой для восстановления пароля'})
        except CustomUser.DoesNotExist:
            # import pdb; pdb.set_trace()
            return Response(
                {'password_recovery_error': ['Пользователь не найден']})
        except SMTPException:
            return Response(
                {'password_recovery_error': 'Ошибка отправки, обратитесь к администратору сайта'}
            )
    else:
        errors = [v[0] for k, v in form.errors.items()]
        return Response(
            {'password_recovery_error': errors}, status=HTTP_200_OK)

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
            # Token.objects.filter(user_id__exact=user.pk).delete()
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

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def refresh_edo_token(request):
    user = request.user
    # auth = unicode(request.auth)
    user.refresh_edo_token()
    # print('edo_token_refreshed')
    return Response({
        'edo_token': user.userprofile.edo_token,
        'edo_token_created': user.userprofile.edo_token_created,
        })