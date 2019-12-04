from django.urls import path, reverse_lazy
# from django.contrib.auth import views as auth_views

from . import views as users

app_name = 'users'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', users.logout, name='logout'),
    # path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    # path('profile_update/', views.UserUpdateView.as_view(), name='profile_update'),
    # path(
    #     'password_change/',
    #     auth_views.PasswordChangeView.as_view(template_name='users/password_change.html',
    #                                           success_url=reverse_lazy('users:password_change_done')),
    #     name='password_change'
    # ),
    # path(
    #     'password_change_done/',
    #     auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
    #     name='password_change_done'
    # ),
]