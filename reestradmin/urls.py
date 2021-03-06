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
    path('csp_groups/', reestradmin.csp_groups, name='csp_groups'),
    path('csp_add_group/', reestradmin.csp_add_group, name='csp_add_group'),
    path('webinars/', reestradmin.webinars, name='webinars'),
    path('user_ul_profile/', reestradmin.user_ul_profile, name='user_ul_profile'),
    path('spks_user_applications/', reestradmin.spks_user_applications, name='spks_user_applications'),
    path('spks_cok_applications/', reestradmin.spks_cok_applications, name='spks_cok_applications'),
    path('spks_new_application/', reestradmin.spks_new_application, name='spks_new_application'),
    path('spks_new_group/', reestradmin.spks_new_group, name='spks_new_group'),
    path('spks_user_certificates/', reestradmin.spks_user_certificates, name='spks_user_certificates'),
    path('center_org_edit/', reestradmin.center_org_edit, name='center_org_edit'),
]

