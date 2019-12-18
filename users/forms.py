from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser, EdoUser


class CustomLoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

    def confirm_login_allowed(self, user):
        pass

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(u'Пользователь "%s" был ранее зарегистрирован' % email)
        return email

class EdoUserCreationForm(UserCreationForm):

    class Meta:
        model = EdoUser
        fields = ('identifier',)

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        if EdoUser.objects.exclude(pk=self.instance.pk).filter(identifier=identifier).exists():
            raise forms.ValidationError(u'Пользователь "%s" был ранее зарегистрирован' % identifier)
        return identifier

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     password_validation.validate_password(password, self.instance)
    #     return password

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #     return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)