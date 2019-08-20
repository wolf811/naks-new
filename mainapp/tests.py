from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory, Client
from django.core.files import File
from django.urls import resolve, reverse
from django.shortcuts import get_object_or_404
from mixer.backend.django import mixer
from mainapp.models import *
import re
import mainapp.views as mainapp
from functools import wraps
import pytest, os

# Create your tests here.
# for r, d, f in os.walk(os.path.join(os.getcwd(), 'media')):
#     for file in f:
#         if file.startswith(('img', 'document', 'file')) and len(file) > 13:
#             os.remove(os.path.join(r, file))

def measure_time(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            # print(f"Execution time of {func.__name__}: {end_ if end_ > 0 else 0} ms")
            timing_report[func.__name__] = end_ if end_ > 0 else 0
    return _time_it

class MockSuperUser:
    def has_perm(self, perm):
        return True

class SiteTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main_page_loads_without_errors(self):
        response = self.client.get(reverse('index'))
        html = response.content.decode('utf8')
        self.assertTrue(html.strip().startswith('<!doctype html>'))
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'mainapp/index.html')

    def test_news_details_opens_by_url(self):
        posts = mixer.cycle(5).blend(Post, active=True)
        for post in posts:
            url = reverse('news_details', kwargs={'pk': post.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.context['post'], Post))
            self.assertEqual(post.title, response.context['post'].title)

# ##########################
# #######pytest tests#######
# ##########################

def test_html_in_contacts(client, rf):
    response = client.get(reverse('contacts'))
    html = response.content.decode('utf8')
    assert html.strip().startswith('<!doctype html>') is True
    request = rf.get('/contacts/')
    response = mainapp.contacts(request)
    assert response.status_code == 200


def test_status_code_of_admin_page(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_request_factory_of_index_view(rf):
    """rf - is an instance of django.test.RequestFactory"""
    request = rf.get('/')
    response = mainapp.index(request)
    assert response.status_code == 200


def test_can_make_posts(db):
    posts = mixer.cycle(3).blend(Post)
    assert len(posts) == 3


def test_can_open_news_page(rf, db):
    request = rf.get('/news')
    response = mainapp.news(request)
    assert response.status_code == 200


def test_can_open_news_details(rf, db):
    post = mixer.blend(Post)
    request = rf.get('/news_details/{}'.format(post.pk))
    response = mainapp.news_details(request, post.pk)
    assert response.status_code == 200


def test_can_open_agreements(rf):
    request = rf.get('/agreement/')
    response = mainapp.agreement(request)
    assert response.status_code == 200


def test_can_open_sasv_page(rf):
    request = rf.get('/sasv/')
    response = mainapp.sasv(request)
    assert response.status_code == 200


def test_can_open_all_static_pages(rf):

    views = {
        '/sasv_ac/': mainapp.sasv_ac,
        '/sasv_acsm/': mainapp.sasv_acsm,
        '/sasv_acso/': mainapp.sasv_acso,
        '/sasv_acst/': mainapp.sasv_acst,
        '/sasv_br1gac/': mainapp.sasv_br1gac,
        '/sasv_docs/': mainapp.sasv_docs,
        '/sasv_nts/': mainapp.sasv_nts,
        '/sasv_helpInfo/': mainapp.sasv_helpInfo,
        '/sasv_openNaks/': mainapp.sasv_openNaks,
        '/sasv_docs/': mainapp.sasv_docs,
        '/sasv_reestr_staff/': mainapp.sasv_reestr_staff,
        '/sasv_reestr_sm/': mainapp.sasv_reestr_sm,
        '/sasv_reestr_so/': mainapp.sasv_reestr_so,
        '/sasv_reestr_st/': mainapp.sasv_reestr_st,
        '/sro/': mainapp.sro,
        '/sro_activity/': mainapp.sro_activity,
        '/sro_docs/': mainapp.sro_docs,
        '/sro_reestr/': mainapp.sro_reestr,
        '/sro_sobranie/': mainapp.sro_sobranie,
        '/sro_presidium/': mainapp.sro_presidium,
        '/sro_president/': mainapp.sro_president,
        '/sro_control_comitet/': mainapp.sro_control_comitet,
        '/sro_disciplinary_comitet/': mainapp.sro_disciplinary_comitet,
        '/sro_audit_commission/': mainapp.sro_audit_commission,
        '/sro_legislation/': mainapp.sro_legislation,
        '/sro_forms_docs/': mainapp.sro_forms_docs,
        '/tk364/': mainapp.tk364,
        '/spks/': mainapp.spks,
        '/spks_docs/': mainapp.spks_docs,
        '/spks_reestr_svid/': mainapp.spks_reestr_svid,
        '/sds/': mainapp.sds,
        '/sds_docs/': mainapp.sds_docs,
        '/sds_reestr_staff/': mainapp.sds_reestr_staff,
        '/sds_reestr_sm/': mainapp.sds_reestr_sm,
        '/sds_reestr_so/': mainapp.sds_reestr_so,
        '/sds_reestr_st/': mainapp.sds_reestr_st,
    }

    for request in views.keys():
        response = views[request](request)
        assert response.status_code == 200


def test_admin_log_in(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_can_create_and_publish_posts(db, client):
    # response = client.get(reverse('contacts'))
    # html = response.content.decode('utf8')
    # assert html.strip().startswith('<!doctype html>') is True
    post = mixer.blend(
        Post,
        active=True,
        main_picture=File(open('media/img_1.jpg', 'rb')),
        short_description=mixer.RANDOM,
        )
    assert Post.objects.first().pk == post.pk
    response = client.get(reverse('news'))
    html = response.content.decode('utf8')
    assert post.title in html
    assert post.main_picture.url in html
    assert post.short_description in html