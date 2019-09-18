# from django.test import TestCase
import pytest
from .models import *
from mixer.backend.django import mixer
import reestr.views as reestr
from django.urls import reverse
from mock import patch

# Create your tests here.

@pytest.mark.reestr
@pytest.mark.django_db
class TestClass:
    org_names = [
        'ООО Сварка трубопроводов',
        'ООО Аттестационный центр',
        'ООО АЦ Сварка'
        ]
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

    def context(self, call_args):
        args, kwargs = call_args
        request_mock, template, context = args
        return context

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
        for org in self.org_names:
            mixer.blend(SROMember, short_name=org, status='a')
        personal_centers = mixer.cycle(5).blend(
            AccreditedCenter, direction='personal', sro_member__status='a')
        inactive_sro_centers_personal = mixer.cycle(5).blend(
            AccreditedCenter, direction='personal', sro_member__status='na')
        inactive_by_status_centers = mixer.cycle(5).blend(
            AccreditedCenter,
            active=False,
            direction='personal',
            sro_member=SROMember.objects.filter(short_name__in=self.org_names).first()
        )
        request = rf.get('/reestr/centers/')
        response = reestr.centers(request, direction='personal')
        html = response.content.decode('utf8')
        for center in personal_centers:
            assert center.short_code in html

        for center in inactive_sro_centers_personal:
            assert center.short_code in html

        for center in inactive_by_status_centers:
            assert center.short_code in html

    @patch('reestr.views.render')
    def test_inactive_and_active_centers_are_different(self, mock_render, rf):
        orgs = mixer.cycle(5).blend(SROMember, status='a')
        for org in orgs:
            mixer.blend(AccreditedCenter, sro_member=org, active=True)
            mixer.blend(AccreditedCenter, sro_member=org, active=False)
        active_centers = AccreditedCenter.objects.filter(active=True)
        inactive_centers = AccreditedCenter.objects.filter(active=False)
        request = rf.get('/reestr/centers/')
        response = reestr.centers(request, direction='personal')
        context = self.context(mock_render.call_args)
        for center in active_centers:
            assert center in context['active_centers']['left'] or\
                center in context['active_centers']['right']
            assert center not in context['inactive_centers']['left'] or\
                center not in context['inactive_centers']['right']
        for center in inactive_centers:
            assert center in context['inactive_centers']['left'] or\
                center in context['inactive_centers']['right']
            assert center not in context['active_centers']['left'] or\
                center not in context['inactive_centers']['right']

    # @patch('reestr.views.render')
    # def test_sro_member_shutdown_leads_to_center_inactivity(self, mock_render, rf):










