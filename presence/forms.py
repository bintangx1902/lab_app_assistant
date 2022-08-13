from django import forms
from django.apps import apps

from .models import *

Files = apps.get_model('file_control', 'Files')


class UserCompletionForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserDataCompleteForms(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['nim', 'phone_number']


class UploadFileForms(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file']
