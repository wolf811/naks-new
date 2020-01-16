from django import forms

from .models import *

class RegistryRecordPersonalForm(forms.ModelForm):
    class Meta:
        model = RegistryRecordPersonal
        fields = (
            'fio', 'data', 'active_since',
            'active_until', 'extension_date'
            )