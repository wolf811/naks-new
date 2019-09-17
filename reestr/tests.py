# from django.test import TestCase
import pytest
from .models import *
from mixer.backend.django import mixer
import reestr.views as reestr
from django.urls import reverse

# Create your tests here.

@pytest.mark.reestr
@pytest.mark.django_db
class TestClass:
    org_names = ['ООО Сварка трубопроводов', 'ООО Аттестационный центр']
    sp_center_accred_details = {
        "name": "cr4gac",
        "gtu": "ГДО, НГДО, ОХНВП",
        "weldtypes": "РД, МП, ААД, АПГ",
        "levels": "I, II, III"
    }

    sm_center_accred_details = {
        "name": "acsm14",
        "gtu": "ГДО, НГДО, ОХНВП",
        "sm_types": "Пп, Пс, Гг, Гз"
    }

    def test_reestr_models(self):
        # WeldType, Activity, GTU, LEVEL, SO, SM, PS
        # PK, City, SROMember, CheckProtocol, AccreditedCenter
        reestr_models = [
            WeldType,
            Activity,
            GTU,
            Level,
            SO,
            SM,
            PS,
            PK,
            City,
            SROMember,
            CheckProtocol,
            AccreditedCenter
        ]

        for model in reestr_models:
            mixer.cycle(2).blend(model)
            assert model.objects.all().count() == 2

    def test_model_return_self_str_attribute(self):
        reestr_models_str = [
            (WeldType, 'short_name'),
            (Activity, 'short_name'),
            (GTU, 'short_name'),
            (Level, 'level'),
            (SO, 'short_name'),
            (SM, 'short_name'),
            (PS, 'short_name'),
            (PK, 'short_name'),
            (City, 'title'),
            (SROMember, 'short_name'),
            (CheckProtocol, 'name'),
            (AccreditedCenter, 'short_code'),
            (AccreditedCertificationPoint, 'point_short_code')
        ]

        for model in reestr_models_str:
            instance = mixer.blend(model[0])
            attr_name = model[1]
            if attr_name == 'short_name':
                assert str(instance) == instance.short_name
            if attr_name == 'name':
                assert str(instance) == instance.name
            if attr_name == 'level':
                assert str(instance) == instance.level
            if attr_name == 'title':
                assert str(instance) == instance.title
            if attr_name == 'short_code':
                assert str(instance) == instance.short_code
            if attr_name == 'point_short_code':
                assert str(instance) == instance.point_short_code

    def test_reestr_of_centers_accessable_by_url(self, rf):
        request = rf.get('/reestr/centers/')
        response = reestr.centers(request, direction='personal')
        assert response.status_code == 200

    def test_reestr_of_ac_filled_with_centers_by_direction(self, rf):
        personal_centers = mixer.cycle(5).blend(
            AccreditedCenter, direction='personal', sro_member__status='a')
        inactive_centers_personal = mixer.cycle(5).blend(
            AccreditedCenter, direction='personal', sro_member__status='na')
        request = rf.get('/reestr/centers/')
        response = reestr.centers(request, direction='personal')
        html = response.content.decode('utf8')
        for center in personal_centers:
            assert center.short_code in html

        for center in inactive_centers_personal:
            assert center.short_code in html





