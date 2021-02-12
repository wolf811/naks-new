from django.urls import path
import control.views as control
app_name = 'control'

urlpatterns = [
    path('base/', control.base, name='base'),
    path('acpnk_profile/', control.acpnk_profile, name='acpnk_profile'),
]