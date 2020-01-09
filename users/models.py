from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import requests

from django.core.mail import send_mail


# Create your models here.

from .managers import CustomUserManager, EdoUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def refresh_edo_token(self):
        try:
            userprofile = self.userprofile
            #     'AUTH_ID': 'popov@naks.ru' #TODO: fix this
            refresh_token_url = 'https://ac.naks.ru/auth/external/check.php?token={}&refresh={}&AUTH_ID=popov@naks.ru'\
                .format(
                    userprofile.edo_token, userprofile.edo_refresh_token
                )
            fresh_token = requests.post(refresh_token_url).content.decode('utf8')
            new_edo_refresh_token, new_edo_token = tuple(fresh_token.split("."))
            userprofile.edo_token = new_edo_token
            userprofile.edo_refresh_token = new_edo_refresh_token
            userprofile.edo_token_created = timezone.now()
            self.save()
            print('USERPROFILE EDO TOKEN REFRESHED', self, self.userprofile)

        except Exception as e:
            print('REFRESHING TOKEN EXCEPTION', e)
            send_mail(
                "EDO refreshing token error",
                "USER: {}, USER PROFILE: {}".format(self.email, self.userprofile),
                "noreply@naks.ru",
                ['popov@naks.ru'],
                fail_silently=True
            )
            pass

class EdoUser(CustomUser):
    identifier = models.CharField(_('identifier'), max_length=20, unique=True)
    USERNAME_FIELD = 'identifier'
    objects = EdoUserManager()


class UserProfile(models.Model):
    STATUS_CHOICES = (
        ('UL', 'Юридическое лицо'),
        ('FL', 'Физическое лицо')
    )
    status = models.CharField(
        u'Юридический статус',
        choices=STATUS_CHOICES,
        default="UL", max_length=2)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    edo_token = models.CharField(u'Основной токен ЭДО', max_length=50, blank=True, null=True)
    edo_refresh_token = models.CharField(u'Токен обновления', max_length=50, blank=True, null=True)
    edo_token_created = models.DateTimeField(
        u'Время создания основного токена',
        null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return 'Profile of {}'.format(self.user)

    def save(self, *args, **kwargs):
        if self.edo_token and not self.edo_token_created:
            self.edo_token_created = timezone.now()
        # super(EdoUser, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

@receiver(post_save, sender=EdoUser)
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=EdoUser)
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

