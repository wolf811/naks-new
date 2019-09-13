from django.db import models

# Create your models here.


class WeldType(models.Model):
    # способ сварки (СП, СТ)
    # short_name
    # full_name
    # international_short_name
    # international_full_name
    short_name = models.CharField(u'Краткое название', max_length=15)
    full_name = models.CharField(u'Расшифровка', max_length=150)
    number = models.SmallIntegerField(u'Порядок сортировки', null=True, blank=True)

    class Meta:
        verbose_name = 'Способ сварки'
        verbose_name_plural = 'Способы сварки'

    def __str__(self):
        return self.short_name


class Activity(models.Model):
    # только для II-IV уровней
    # руководство и технический контроль за проведением сварочных работ
    # участие в работе органов по подготовке и аттестации
    pass


class GTU(models.Model):
    # ГРУППЫ ТУ
    pass


class Level(models.Model):
    # I-IV
    pass


class SO(models.Model):
    pass


class SM(models.Model):
    pass


class PS(models.Model):
    pass


class PK(models.Model):
    # code NOK
    # title
    pass


class SROMember(models.Model):
    # name
    # phone
    # email
    # address
    pass


class Center(models.Model):
    # active_since
    # active_until
    pass

