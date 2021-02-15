from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from stdimage.models import StdImageField


# Create your models here.

class Tag(models.Model):
    name = models.CharField(u'Название тэга', max_length=100)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(u'Название раздела', max_length=100)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Post(models.Model):
    """model for publications"""
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150, verbose_name='Заголовок публикации')
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок публикации', blank=True, default='')
    short_description = RichTextUploadingField(verbose_name='Краткий текст', blank=True, null=True)
    full_description = RichTextUploadingField(verbose_name='Подробный текст', blank=True, null=True)
    # main_picture = models.ImageField(verbose_name='Главная картинка', upload_to='post_images', blank=True, null=True)
    main_picture = StdImageField(
        u'Главная картинка публикации',
        null=True,
        blank=True,
        upload_to='post_images/',
        variations={
            'thumbnail': {"width": 200, "height": 100, "crop": True},
            'medium': {"width": 1024, "height": 768, "crop": True},
            'large': {"width": 1920, "height": 1080, "crop": True}
        }
    )
    published_date = models.DateTimeField(u'Дата публикации', default=timezone.now)
    active = models.BooleanField(u'Опубликована', default=True)
    mark_as_announcement = models.BooleanField(u'Отметить как анонс события', default=False)
    publish_in_side_panel= models.BooleanField(
        verbose_name="Опубликовать в боковой панели", default=False
    )
    spread_over_api = models.BooleanField(
        verbose_name="Распространить по сайтам АЦ", default=False
    )

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return 'Публикация {}, дата {}'.format(self.title, self.published_date)

    def get_absolute_url(self):
        return reverse("news_details", kwargs={"pk": self.pk})


class Banner(models.Model):
    """banners for main page"""
    title = models.CharField(u'Название баннера', max_length=100)
    short_description = models.CharField(u'Краткое описание', max_length=100)
    short_description_url = models.URLField(u'Ссылка', blank=True, null=True)
    # image = models.ImageField(u'Картинка для баннера', upload_to='banner_images/')
    image = StdImageField(
        u'Картинка для фона баннера',
        upload_to='banner_images/',
        variations={
            'thumbnail': {"width": 200, "height": 100, "crop": True},
            'large': {"width": 1920, "height": 1080, "crop": True}
        }
    )
    number = models.SmallIntegerField(verbose_name='Порядок вывода', default=0)
    active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.title


class Photo(models.Model):
    """model for handling photos"""
    # image = models.ImageField(u'Фото', upload_to='photos/')
    image = StdImageField(
        u'Картинка для публикации',
        upload_to='post_images/',
        variations={
            'thumbnail': {"width": 200, "height": 100, "crop": True},
            'medium': {"width": 1024, "height": 768, "crop": True},
            'large': {"width": 1920, "height": 1080, "crop": True}
        }
    )
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    number = models.SmallIntegerField(verbose_name='Порядок вывода', default=0)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return 'picture {}'.format(self.pk)


class Document(models.Model):
    """model for upload and store documents"""
    title = models.CharField(u'Название документа', max_length=200)
    file = models.FileField(u'Файл', upload_to='documents/')
    tags = models.ManyToManyField(Tag)
    main_page_rotation = models.BooleanField(u'Включить в ротацию на главной', default=False)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title


class Partner(models.Model):
    """model for partners page"""
    title = models.CharField(u'Название', max_length=200)
    logotype = models.FileField(u'Логотип', upload_to='partners_logotypes/')

    class Meta:
        # verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    def __str__(self):
        return self.title


class ContactSubdivision(models.Model):
    number = models.SmallIntegerField(u'Порядок вывода отдела', blank=True, null=True)
    title = models.CharField(u'Название отдела', max_length=50)
    subtitle = models.CharField(u'Подзаголовок', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы (для контактов)'

    def __str__(self):
        return self.title


class Contact(models.Model):
    """model for contacts handling"""
    subdivision = models.ForeignKey(ContactSubdivision, null=True, blank=True, on_delete=models.SET_NULL)
    number = models.SmallIntegerField(u'Порядок вывода на сайт', blank=True, null=True)
    name = models.CharField(u'ФИО', max_length=100)
    description = models.CharField(u'Описание (например, "к.т.н.")', max_length=100)
    phone = models.CharField(u'Номер телефона', max_length=50, default='')
    phone_secondary = models.CharField(u'Второй номер телефона (необязательно)', max_length=50, blank=True, null=True)
    email = models.EmailField(u'Адрес электронной почты', blank=True, null=True)
    active = models.BooleanField(u'Активен', default=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return '{}, {}'.format(self.name, self.description)


class OrgProfile(models.Model):
    short_name = models.CharField(u'Краткое название компании', max_length=80, default='')
    full_name = models.CharField(u'Полное название компании', max_length=80, default='')
    phone = models.CharField(u'Номер телефона', max_length=50, default='')
    phone_secondary = models.CharField(u'Второй номер телефона (необязательно)', max_length=50, blank=True, null=True)
    email = models.EmailField(u'Адрес электронной почты', blank=True, null=True)
    description = models.TextField(u'Описание, история создания', blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.short_name
