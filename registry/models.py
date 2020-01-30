from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.utils import timezone


# Create your models here.
class Company(models.Model):
    name = models.CharField(u'Организация', max_length=500, unique=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name


class RegistryRecord(models.Model):
    STATUS_LIST = ((0, 'new'), (1, 'not_published'), (2, 'published'), (3, 'canceled'))
    status = models.IntegerField(u'Статус', default=0, choices=STATUS_LIST)
    edo_id = models.PositiveIntegerField(
        u'Идентификатор ЭДО', null=True, blank=True, unique=True)
    title = models.CharField(
        u'Название записи', max_length=64, blank=True, null=True)
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL, db_index=True)
    date_created = models.DateField(
        u'Дата создания записи', default=timezone.now)
    data = JSONField(u'JSON-данные', blank=True, null=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['company', 'data']),
            GinIndex(name='data_json_index', fields=['data'], opclasses=['jsonb_path_ops'])
        ]


class RegistryRecordPersonal(RegistryRecord):
    fio = models.CharField(u'ФИО', max_length=100, db_index=True)
    active_since = models.DateField(u'Дата аттестации', null=True, blank=True)
    active_until = models.DateField(u'Дата окончания аттестации', null=True, blank=True, db_index=True)
    extension_date = models.DateField(u'Дата продления', null=True, blank=True, db_index=True)
    center = models.ForeignKey('registry.RegistryRecordPersonal', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        indexes = [
            models.Index(fields=['-active_since',]),
            models.Index(fields=['fio',]),
        ]


    def __str__(self):
        return self.fio


class RegistryRecordMaterials(RegistryRecord):
    svid_number = models.CharField(u'Номер свидетельства', max_length=20)
    active_since = models.DateField(u'Дата аттестации', null=True, blank=True)
    active_until = models.DateField(u'Дата окончания аттестации', null=True, blank=True)

    def __str__(self):
        return self.svid_number



#class RegistryRecordMaterials(RegistryRecord)
#class RegistryRecordEquipment(RegistryRecord)