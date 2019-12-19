from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


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

    def save(self, *args, **kwargs):
        if self.edo_token:
            self.edo_token_created = timezone.now()
        super(EdoUser, self).save(*args, **kwargs)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# @receiver(post_delete, sender=CustomUser)
# def delete_user_profile(sender, instance, **kwargs):
#     instance.userpofile.delete()
