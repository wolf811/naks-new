# from django.test import TestCase
import pytest
from .models import *
from mixer.backend.django import mixer
import reestr.views as reestr
from django.urls import reverse
from mock import patch
from itertools import chain

# Create your tests here.


def combined(*arrs):
    comb = list(chain(*arrs))
    return comb


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

    # mock views context to use with request factory
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
            # PS,
            # PK,
            City,
            SROMember,
            CheckProtocol,
            AccreditedCenter
        ]

        for model in reestr_models:
            mixer.cycle(2).blend(model)
            assert model.objects.all().count() == 2

    def test_model_return_self_str_attribute(self):
        # Check all str(model) at once
        reestr_models_str = [
            (WeldType, 'short_name'),
            (Activity, 'short_name'),
            (GTU, 'short_name'),
            (Level, 'level'),
            (SO, 'short_name'),
            (SM, 'short_name'),
            # (PS, 'short_name'),
            # (PK, 'short_name'),
            (City, 'title'),
            (SROMember, 'short_name'),
            (CheckProtocol, 'name'),
            (AccreditedCenter, 'short_code'),
            (AccreditedCertificationPoint, 'short_code')
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
            sro_member=SROMember.objects.filter(
                short_name__in=self.org_names).first()
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
    def test_centers_are_in_different_context(self, mock_render, rf):
        orgs = mixer.cycle(5).blend(SROMember, status='a')
        counter = 0
        for org in orgs:
            mixer.blend(
                AccreditedCenter,
                short_code=mixer.sequence("active_{}".format(counter)),
                sro_member=org,
                active=True
                )
            mixer.blend(
                AccreditedCenter,
                short_code=mixer.sequence("inactive_{}".format(counter)),
                sro_member=org,
                active=False
                )
            mixer.blend(
                AccreditedCenter,
                short_code=mixer.sequence("suspended_{}".format(counter)),
                sro_member=org,
                temporary_suspend_date=mixer.RANDOM
            )
            counter += 1
        active_centers = AccreditedCenter.objects.filter(
            active=True, temporary_suspend_date__isnull=True)
        inactive_centers = AccreditedCenter.objects.filter(active=False)
        suspended_centers = AccreditedCenter.objects.filter(
            temporary_suspend_date__isnull=False)
        request = rf.get('/reestr/centers/')
        response = reestr.centers(request, direction='personal')
        context = self.context(mock_render.call_args)
        active_centers_cntxt = combined(
            context['active_centers']['left'],
            context['active_centers']['right']
        )
        inactive_centers_cntxt = combined(
            context['inactive_centers']['left'],
            context['inactive_centers']['right']
        )
        suspended_centers_cntxt = combined(
            context['suspended_centers']['left'],
            context['suspended_centers']['right']
        )
        for center in active_centers:
            assert center in active_centers_cntxt and\
                center not in inactive_centers_cntxt and\
                center not in suspended_centers_cntxt
        for center in inactive_centers:
            assert center in inactive_centers_cntxt and\
                center not in active_centers_cntxt and\
                center not in suspended_centers_cntxt
        for center in suspended_centers:
            assert center in suspended_centers_cntxt and\
                center not in active_centers_cntxt and\
                center not in inactive_centers_cntxt

    @patch('reestr.views.render')
    def test_member_shutdown_cause_to_center_inactivity(self, mock_render, rf):
        org = mixer.blend(SROMember, status='a')
        active_centers = mixer.cycle(5).blend(
            AccreditedCenter,
            active=True,
            sro_member=org,
            direction='personal'
            )
        # now shutdown_org
        org.status = 'na'
        org.save()
        request = rf.get('/reestr/centers/')
        response = reestr.centers(request, direction='personal')
        context = self.context(mock_render.call_args)
        for c in active_centers:
            assert c in combined(
                context['inactive_centers']['left'],
                context['inactive_centers']['right']
                )

    @patch('reestr.views.render')
    def test_filter_parameters_passed_to_reestr_page_context(self, mock_render, rf):
        weldtypes = mixer.cycle(10).blend(WeldType)
        gtus = mixer.cycle(10).blend(GTU)
        levels = mixer.cycle(4).blend(Level)
        request = rf.get('/reestr/centers/')
        response = reestr.centers(request, direction='personal')
        context = self.context(mock_render.call_args)
        for weld in weldtypes:
            assert weld in context['weld_types']
        for gtu in gtus:
            assert gtu in context['gtus']
        for level in levels:
            assert level in context['levels']








