from django.urls import path
import reestr.views as reestr
app_name = 'reestr'

urlpatterns = [
    path('centers/<slug:direction>', reestr.centers, name='centers'),
]