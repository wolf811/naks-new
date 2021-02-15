from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from mainapp.models import Post



# Create your models here.
class DocumentCategory(models.Model):
    name = models.CharField(u'Категория документов (например, персонал)', max_length=64)
    number = models.SmallIntegerField(verbose_name='Порядок сортировки',
                                    null=True, blank=True, default=None)

    class Meta:
        verbose_name = "Категория документа"
        verbose_name_plural = "Категории документов"

    def __str__(self):
        return self.name

class Document(models.Model):
    """"
    эта модель используется для
    загрузки документов в базу данных
    """
    title = models.CharField(u'Название', max_length=500)
    document = models.FileField(verbose_name='Документ',
                                upload_to="documents/",
                                validators=[FileExtensionValidator(
                                    allowed_extensions=[
                                        'pdf', 'docx', 'doc', 'jpg', 'jpeg'],
                                    message="Неправильный тип файла, используйте\
                                        PDF, DOCX, DOC, JPG, JPEG")])

    category = models.ForeignKey(DocumentCategory, blank=True, null=True, on_delete=models.SET_NULL)
    url_code = models.CharField(u'Код ссылки', max_length=30, blank=True, default='НЕ УКАЗАН')
    data = JSONField(u'JSON-данные', blank=True, null=True)
    uploaded_at = models.DateTimeField(
        verbose_name='Загружен', default=timezone.now)
    # tags = models.ManyToManyField(Tag, verbose_name='Тэги', blank=True)
    created_date = models.DateTimeField(
        default=timezone.now, verbose_name='Дата создания')
    post = models.ForeignKey(Post, verbose_name='Страница',
                             blank=True, default='',
                             on_delete=models.SET_NULL,
                             null=True)
    publish_on_main_page = models.BooleanField(
        verbose_name="Опубиковать на главной", default=False)
    publish_in_side_panel= models.BooleanField(
        verbose_name="Опубликовать в боковой панели", default=False
    )
    spread_over_api = models.BooleanField(
        verbose_name="Распространить по сайтам АЦ", default=False
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension


def upload_to(instance, filename):
    """left for future, unused function"""
    filename_base, filename_ext = os.path.splitext(filename)
    return "upload/{post_pk}/{filename}{extension}".format(
        post_pk=instance.pk,
        filename=slugify(filename_base),
        extension=filename_ext.lower(),)


def get_image_filename():
    """unused function, left for future"""
    return 'image_{}'.format(slugify(timezone.now()))