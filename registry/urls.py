from django.urls import path
# from django.urls import path, reverse_lazy
# from django.contrib.auth import views as auth_views

from . import views as registry

app_name = 'users'

urlpatterns = [
    path('personal/', registry.personal, name='personal'),
    path('import/<year>', registry.initiate_import, name='import'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', users.logout_request, name='logout'),
    # path('register/', users.register_request, name='register'),
    # path('recover-password/', users.recover_password_request, name='recover-password'),
    # path('update-password/<uid>/<token>', users.update_password, name='update-password'),
    # path('refresh-edo-token/', users.refresh_edo_token, name='refresh-edo-token'),
]