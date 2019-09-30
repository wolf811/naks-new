"""naks_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path, include
import mainapp.views as mainapp
import reestr.views as reestr

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from mainapp.sitemap import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', mainapp.PostViewSet)
router.register(r'centers', reestr.CentersViewSet)
router.register(r'dirs', reestr.DirectoriesViewSet, basename='directories')

sitemaps = {
    'posts': PostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.index, name='index'),
    path('agreement/', mainapp.agreement, name='agreement'),
    path('contacts/', mainapp.contacts, name='contacts'),
    path('news/', mainapp.news, name='news'),
    path('news_details/<slug:pk>', mainapp.news_details, name='news_details'),
    path('sasv/', mainapp.sasv, name='sasv'),
    path('sasv_ac/', mainapp.sasv_ac, name='sasv_ac'),
    path('sasv_acsm/', mainapp.sasv_acsm, name='sasv_acsm'),
    path('sasv_acso/', mainapp.sasv_acso, name='sasv_acso'),
    path('sasv_acst/', mainapp.sasv_acst, name='sasv_acst'),
    path('sasv_br1gac/', mainapp.sasv_br1gac, name='sasv_br1gac'),
    path('sasv_helpInfo/', mainapp.sasv_helpInfo, name='sasv_helpInfo'),
    path('sasv_nts/', mainapp.sasv_nts, name='sasv_nts'),
    path('sasv_openNaks/', mainapp.sasv_openNaks, name='sasv_openNaks'),
    path('sasv_docs/', mainapp.sasv_docs, name='sasv_docs'),
    path('sasv_reestr_staff/', mainapp.sasv_reestr_staff, name='sasv_reestr_staff'),
    path('sasv_reestr_sm/', mainapp.sasv_reestr_sm, name='sasv_reestr_sm'),
    path('sasv_reestr_so/', mainapp.sasv_reestr_so, name='sasv_reestr_so'),
    path('sasv_reestr_st/', mainapp.sasv_reestr_st, name='sasv_reestr_st'),
    path('sro/', mainapp.sro, name='sro'),
    path('sro_activity/', mainapp.sro_activity, name='sro_activity'),
    path('sro_docs/', mainapp.sro_docs, name='sro_docs'),
    path('sro_reestr/', mainapp.sro_reestr, name='sro_reestr'),
    path('sro_sobranie/', mainapp.sro_sobranie, name='sro_sobranie'),
    path('sro_presidium/', mainapp.sro_presidium, name='sro_presidium'),
    path('sro_president/', mainapp.sro_president, name='sro_president'),
    path('sro_control_comitet/', mainapp.sro_control_comitet, name='sro_control_comitet'),
    path('sro_disciplinary_comitet/', mainapp.sro_disciplinary_comitet, name='sro_disciplinary_comitet'),
    path('sro_audit_commission/', mainapp.sro_audit_commission, name='sro_audit_commission'),
    path('sro_legislation/', mainapp.sro_legislation, name='sro_legislation'),
    path('sro_forms_docs/', mainapp.sro_forms_docs, name='sro_forms_docs'),
    path('tk364/', mainapp.tk364, name='tk364'),
    path('spks/', mainapp.spks, name='spks'),
    path('spks_docs/', mainapp.spks_docs, name='spks_docs'),
    path('spks_reestr_svid/', mainapp.spks_reestr_svid, name='spks_reestr_svid'),
    path('sds/', mainapp.sds, name='sds'),
    path('sds_docs/', mainapp.sds_docs, name='sds_docs'),
    path('sds_reestr_staff/', mainapp.sds_reestr_staff, name='sds_reestr_staff'),
    path('sds_reestr_sm/', mainapp.sds_reestr_sm, name='sds_reestr_sm'),
    path('sds_reestr_so/', mainapp.sds_reestr_so, name='sds_reestr_so'),
    path('sds_reestr_st/', mainapp.sds_reestr_st, name='sds_reestr_st'),
    path('reestr/', include('reestr.urls', namespace='reestr')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('naks_api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)