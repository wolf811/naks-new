from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory, Client
from rest_framework.test import APIRequestFactory
from django.core.files import File
from django.urls import resolve, reverse
from django.shortcuts import get_object_or_404
from mixer.backend.django import mixer
from mainapp.models import *
import re
import mainapp.views as mainapp
from functools import wraps
import pytest, os, json
from stdimage.models import *
import datetime
from mock import patch, MagicMock, Mock
import requests
from rest_framework.test import APIRequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

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


def test_html_in_contacts(client, db, rf):
    response = client.get(reverse('contacts'))
    html = response.content.decode('utf8')
    assert html.strip().startswith('<!doctype html>') is True
    request = rf.get('/contacts/')
    response = mainapp.contacts(request)
    assert response.status_code == 200

@pytest.mark.skip(reason="no way of currently testing this")
def test_status_code_of_admin_page(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_request_factory_of_index_view(rf, db):
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

@pytest.mark.skip(reason="4 default arguments in pytest fixture, but custom model only have 3")
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
    assert post.main_picture.medium.url in html
    assert post.short_description in html

def test_can_retrieve_api_urls_after_publishing_posts(db, client):
    posts = mixer.cycle(3).blend(Post, active=True)
    for post in posts:
        response = client.get('/naks_api/posts/{}/'.format(post.pk))
        # import pdb; pdb.set_trace()
        assert response.status_code == 200
        api_data = json.loads(response.content.decode('utf8'))
        assert api_data['title'] == post.title
        assert api_data['short_description'] == post.short_description


def test_api_contain_images_urls(db, client):
    post = mixer.blend(Post, main_picture=File(open('media/img_1.jpg', 'rb')))
    response = client.get('/naks_api/posts/{}/'.format(post.pk))
    api_data = json.loads(response.content.decode('utf8'))
    assert post.main_picture.thumbnail.url in api_data['image_urls']['thumbnail']
    assert post.main_picture.medium.url in api_data['image_urls']['medium']
    assert post.main_picture.large.url in api_data['image_urls']['large']


def test_can_make_contacts_and_publish_them(db, client):
    subdivision = mixer.blend(ContactSubdivision)
    contacts = mixer.cycle(10).blend(
        Contact,
        subdivision=subdivision,
        phone=mixer.RANDOM,
        email=mixer.RANDOM,
        )
    response = client.get('/contacts/')
    assert response.status_code == 200
    html = response.content.decode('utf8')
    for contact in contacts:
        assert contact.name in html
        assert contact.phone in html
        assert contact.email in html
    assert subdivision.title in html


def test_can_make_banners_and_publish_them(db, rf):
    banner = mixer.blend(Banner, active=True)
    request = rf.get('/')
    response = mainapp.index(request)
    html = response.content.decode('utf8')
    assert banner.title in html
    # check if banner.image has different size, made by StdImage
    assert isinstance(banner.image, StdImageFieldFile)
    assert banner.image.large.url in html


def test_can_make_publications_on_main_page(db, rf):
    post = mixer.blend(
        Post,
        active=True,
        main_picture=File(open('media/img_1.jpg', 'rb'))
    )
    additional_photo = mixer.blend(
        Photo,
        image=File(open('media/img_2.jpg', 'rb')),
        post=post
    )
    request = rf.get('/')
    response = mainapp.index(request)
    html = response.content.decode('utf8')
    assert post.main_picture.medium.url in html
    assert additional_photo.image.medium.url in html


def test_side_panel_posts_available_on_main_page(db, rf):
    dates = []
    for i in range(6):
        dates.append(timezone.now() - datetime.timedelta(days=i))
    for date in dates:
        mixer.blend(
            Post,
            active=True,
            main_picture=File(open('media/img_1.jpg', 'rb')),
            published_date=date,
            full_description=mixer.RANDOM
        )
    request = rf.get('/')
    response = mainapp.index(request)
    html = response.content.decode('utf8')
    all_posts = Post.objects.all().order_by('-published_date')[:6]
    for post in all_posts:
        assert post.title in html
    for post in all_posts[5:6]:
        assert post.main_picture.thumbnail.url in html
        # test details of news
        req_details = rf.get('/news_details/{}/'.format(post.pk))
        res_details = mainapp.news_details(req_details, post.pk)
        html_details = res_details.content.decode('utf8')
        assert res_details.status_code == 200
        assert post.title in html_details
        assert post.subtitle in html_details
        assert post.full_description in html_details
        # TODO: make full-size picture for page-details


# @pytest.mark.django_db
# @patch('mainapp.serializers.PostSerializer.get_image_urls')
def test_news_content_accessable_by_rest_api(db):
    factory = APIRequestFactory()
    post = mixer.blend(
        Post,
        active=True,
        # main_picture=File(open('media/img_3.png', 'rb')),
    )
    request = factory.get('/naks_api/posts/')
    view = mainapp.PostDetailsAPI.as_view()
    response = view(request, pk=post.pk)
    assert response.status_code == 200
    response.render()
    html = response.content.decode('utf8')
    assert post.title in html

# LETS MOCK!
requests = MagicMock()
response = MagicMock()
requests.get.return_value = response
response.status_code = 200
response.ok = True
response.content = b'[\n  {\n    "id": 1,\n    "title": "Post 1"\n  },\
         \n  {\n    "id": 2,\n    "title": "Post 2"\n  },\n  {\n    "id": 3,\n    "title": "Post 3"\n  }\n]'
response.json.return_value = [{'id': 1, 'title': 'Post 1'}, {'id': 2, 'title': 'Post 2'}, {'id': 3, 'title': 'Post 3'}]


def test_with_mock_api_replacement(db):
    ### real url
    url = 'https://my-json-server.typicode.com/testpass1982/fake_rest/posts'
    ### fake_url
    fake_url = 'https://my-json-server.typicode.com/testpass1982/fake_rest/centers/personal/'
    response = requests.get(fake_url)
    # import pdb; pdb.set_trace()
    assert response.ok
    assert response.json() == [
        {'id': 1, 'title': 'Post 1'},
        {'id': 2, 'title': 'Post 2'},
        {'id': 3, 'title': 'Post 3'}
        ]
    # import pdb; pdb.set_trace()
    assert json.loads(response.content.decode('utf8')) == [
        {'id': 1, 'title': 'Post 1'},
        {'id': 2, 'title': 'Post 2'},
        {'id': 3, 'title': 'Post 3'}
        ]


    # mock_response = Mock()
    # mock_response.content = b'[\n  {\n    "id": 1,\n    "title": "Post 1"\n  },\
    #     \n  {\n    "id": 2,\n    "title": "Post 2"\n  },\n  {\n    "id": 3,\n    "title": "Post 3"\n  }\n]'
    # # [{'id': 1, 'title': 'Post 1'}, {'id': 2, 'title': 'Post 2'}, {'id': 3, 'title': 'Post 3'}]
    # # {'id': 1, 'title': 'Post 1'}
