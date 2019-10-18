from django.urls import path
import reestradmin.views as reestradmin
app_name = 'reestr'

urlpatterns = [
    path('', reestradmin.hello, name='hello'),
]