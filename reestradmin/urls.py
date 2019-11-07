from django.urls import path
import reestradmin.views as reestradmin
app_name = 'reestr'

urlpatterns = [
    path('base/', reestradmin.base, name='base'),
    path('centers_list/', reestradmin.centers_list, name='centers_list'),
    path('center_acsm_edit/', reestradmin.center_acsm_edit, name='center_acsm_edit'),
    path('organization_list/', reestradmin.organization_list, name='organization_list'),
    path('organization_edit/', reestradmin.organization_edit, name='organization_edit'),
]

