from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    """model for publications"""
    published_date = models.DateTimeField(u'Дата публикации', default=timezone.now)
    title = models.CharField(max_length=150, verbose_name='Заголовок публикации')
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок публикации', blank=True, default='')
    short_description = RichTextUploadingField(verbose_name='Краткий текст', blank=True)
    full_description = RichTextUploadingField(verbose_name='Подробный текст', blank=True)
    

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return 'Публикация {}, дата {}'.format(self.title, self.published_date)

class Photo(models.Model):
    """model for handling photos"""
    image = models.ImageField(u'Фото', upload_to='upload/')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)