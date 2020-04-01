from django.urls import path
import reestradmin.views as reestradmin
app_name = 'reestr'

urlpatterns = [
    path('base/', reestradmin.base, name='base'),
    path('centers_list/', reestradmin.centers_list, name='centers_list'),
    path('center_acsm_edit/', reestradmin.center_acsm_edit, name='center_acsm_edit'),
    path('organization_list/', reestradmin.organization_list, name='organization_list'),
    path('organization_edit/', reestradmin.organization_edit, name='organization_edit'),
    path('list_instructions/', reestradmin.list_instructions, name='list_instructions'),
    path('instruction_detail/', reestradmin.instruction_detail, name='instruction_detail'),
    path('experts_list/', reestradmin.experts_list, name='experts_list'),
    path('expert_profile/', reestradmin.expert_profile, name='expert_profile'),
    path('certificates_list/', reestradmin.certificates_list, name='certificates_list'),
    path('csp_profile/', reestradmin.csp_profile, name='csp_profile'),
    path('webinars/', reestradmin.webinars, name='webinars'),
]

