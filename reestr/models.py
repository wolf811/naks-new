from django.db import models
from django.utils import timezone
# Create your models here.


class Spr(models.Model):
    short_name = models.CharField(u'Краткое название', max_length=15)
    full_name = models.CharField(u'Расшифровка', max_length=150)
    number = models.SmallIntegerField(u'Порядок сортировки', null=True, blank=True)

    class Meta:
        abstract = True


class WeldType(Spr):
    # способ сварки (СП, СТ)
    # short_name
    # full_name
    # international_short_name
    # international_full_name
    class Meta:
        verbose_name = 'Способ сварки'
        verbose_name_plural = 'Способы сварки'

    def __str__(self):
        return self.short_name


class Activity(Spr):
    # только для II-IV уровней
    # руководство и технический контроль за проведением сварочных работ
    # участие в работе органов по подготовке и аттестации
    class Meta:
        verbose_name = 'Вид деятельности'
        verbose_name_plural = 'Виды деятельности'

    def __str__(self):
        return self.short_name


class GTU(Spr):
    # ГРУППЫ ТУ
    # участие в работе органов по подготовке и аттестации
    class Meta:
        verbose_name = 'Группа ТУ'
        verbose_name_plural = 'Группы ТУ'

    def __str__(self):
        return self.short_name


class Level(models.Model):
    # I-IV
    level = models.CharField(u'Уровень', max_length=2)

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'

    def __str__(self):
        return self.level


class SO(Spr):
    # welding equipment types catalog
    class Meta:
        verbose_name = 'Вид СО'
        verbose_name_plural = 'Виды СО'

    def __str__(self):
        return self.short_name


class SM(Spr):
    # materials types catalog
    class Meta:
        verbose_name = 'Вид СМ'
        verbose_name_plural = 'Виды СМ'

    def __str__(self):
        return self.short_name


class PS(Spr):
    ps_code = models.CharField(u'Код профстандарта', max_length=10)

    class Meta:
        verbose_name = 'Профстандарт'
        verbose_name_plural = 'Профстандарты'

    def __str__(self):
        return self.short_name


class PK(Spr):
    pk_code = models.CharField(u'Код квалификации', max_length=20)
    ps = models.ForeignKey(PS, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Квалификация'
        verbose_name_plural = 'Квалификации'

    def __str__(self):
        return self.short_name


class City(models.Model):
    title = models.CharField(u'Название', max_length=30)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.title


class SROMember(models.Model):
    # name
    # phone
    # email
    # address
    active = 'a'
    not_active = 'na'
    STATUSES = (
        (active, 'Действует'),
        (not_active, 'Исключен')
    )
    short_name = models.CharField(u'Краткое наименование', max_length=50)
    full_name = models.CharField(u'Полное наименование', max_length=200)
    become_member_information = models.CharField(
        u'Информация о включении в реестр НАКС',
        blank=True, null=True, max_length=100)
    become_member_doc_link = models.URLField(
        u'Ссылка на документ о включении в реестр НАКС', blank=True, null=True)
    ur_address = models.CharField(u'Юридический адрес', max_length=200)
    post_address = models.CharField(
        u'Почтовый адрес', null=True, blank=True, max_length=200)
    actual_address = models.CharField(
        u'Фактический адрес', null=True, blank=True, max_length=200)
    city = models.ForeignKey(
        City, null=True, blank=True, on_delete=models.SET_NULL)
    chief = models.CharField(u'ФИО руководителя организации', max_length=100)
    phone = models.CharField(u'Телефон(ы)', max_length=100)
    fax = models.CharField(u'Факс', max_length=50)
    email = models.EmailField(u'Адрес электронной почты', max_length=50)
    svid_number = models.CharField(
        u'Номер свидетельства о членстве', max_length=4)
    status = models.CharField(
        u'Статус', max_length=2, choices=STATUSES, default=active)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации-члены СРО'

    def __str__(self):
        return self.short_name


class CheckProtocol(models.Model):
    name = models.CharField(u'Название документа', max_length=100)
    document = models.FileField(u'Файл', upload_to='documents/')
    date_document = models.DateField(u'Дата документа', default=timezone.now)
    number_document = models.CharField(u'Номер документа', max_length=10)
    member = models.ForeignKey(
        SROMember, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name


class Center(models.Model):
    # active_since
    # active_until
    active = models.BooleanField(u'Активен', default=True)
    active_since = models.DateField(
        u'Дата начала аккредитации', default=timezone.now)
    active_until = models.DateField(
        u'Дата окончания аккредитации', null=True, blank=True)
    temporary_suspend_date = models.DateField(
        u'Временно приостановлен до',
        null=True,
        blank=True
    )
    chief = models.CharField(u'ФИО руководителя центра', max_length=50)
    sro_member = models.ForeignKey(SROMember, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AccreditedCenter(Center):
    materials = 'attsm'
    equipment = 'attso'
    technologies = 'attst'
    personal = 'personal'
    csp = 'specpod'
    qualification = 'qualifications'
    certification = 'cert'
    DIRECTIONS = (
        (personal, 'Аттестация персонала'),
        (csp, 'Специальная подготовка'),
        (materials, 'Аттестация сварочных материалов'),
        (equipment, 'Аттестация сварочного оборудования'),
        (technologies, 'Аттестация сварочных технологий'),
        (qualification, 'Оценка квалификации'),
        (certification, 'Добровольная сертфикация')
    )
    transneft = 'tn'
    gazprom = 'gp'
    SPECIAL_REQUIREMENTS = (
        (transneft, 'Аттестация с учетом требований Транснефть'),
        (gazprom, 'Аттестация с учетом требований Газпром'),
    )

    direction = models.CharField(
        u'Направление деятельности',
        max_length=14,
        choices=DIRECTIONS,
        default=personal
        )

    special = models.CharField(
        u'Особые требования',
        max_length=2,
        choices=SPECIAL_REQUIREMENTS,
        blank=True,
        null=True,
        default=None
    )

    special_tn = models.BooleanField('Доп требования ТН', default=False)
    special_gp = models.BooleanField('Доп требования ГП', default=False)

    short_code = models.CharField(
        u'Шифр центра',
        max_length=10
        )
    weldtypes = models.ManyToManyField(
        WeldType,
        verbose_name='Способы сварки',
        blank=True
        )
    gtus = models.ManyToManyField(
        GTU,
        verbose_name='Группы ТУ',
        blank=True
        )
    levels = models.ManyToManyField(
        Level,
        verbose_name="Уровни",
        blank=True
        )
    acitvities = models.ManyToManyField(
        Activity,
        verbose_name='Виды д-сти',
        blank=True
        )
    sm_types = models.ManyToManyField(
        SM,
        verbose_name="Шифры СО",
        blank=True
        )
    so_types = models.ManyToManyField(
        SO,
        verbose_name="Шифры СМ",
        blank=True
        )
    profstandards = models.ManyToManyField(
        PS,
        verbose_name="Профстандарты",
        blank=True
        )
    profqualifications = models.ManyToManyField(
        PK,
        verbose_name="Профквалификации",
        blank=True
        )

    class Meta:
        verbose_name = 'Аккредитация'
        verbose_name_plural = 'Аккредитации'

    def __str__(self):
        return self.short_code

    def save(self, *args, **kwargs):
        if self.sro_member.status == 'na':
            self.active = False
        super(AccreditedCenter, self).save(*args, **kwargs)


class AccreditedCertificationPoint(AccreditedCenter):
    short_code = None
    point_short_code = models.CharField(u'Шифр АП', max_length=50)
    base_org_name = models.CharField(
        u'Наименование организации', max_length=100)
    base_org_ur_address = models.CharField(
        u'Юридический адрес организации', max_length=100)
    base_actual_address = models.CharField(
        u'Фактический адрес организации', max_length=100)

    class Meta:
        verbose_name = 'Аттестационный пункт'
        verbose_name_plural = 'Аттестационные пункты'

    def __str__(self):
        return self.point_short_code
