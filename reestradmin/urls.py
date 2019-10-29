from django.urls import path
import reestradmin.views as reestradmin
app_name = 'reestr'

urlpatterns = [
    path('base/', reestradmin.base, name='base'),
    path('centers_list/', reestradmin.centers_list, name='centers_list'),
    path('organization_list/', reestradmin.organization_list, name='organization_list'),
    path('organization_profile/', reestradmin.organization_profile, name='organization_profile'),
    path('organization_edit/', reestradmin.organization_edit, name='organization_edit'),
]

