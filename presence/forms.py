from django import forms
from django.apps import apps

from .models import *

Files = apps.get_model('file_control', 'Files')
TokenToResetPassword = apps.get_model('assistant', 'TokenToResetPassword')
StudentScore = apps.get_model('assistant', 'StudentScore')
classification = ['PRETEST', 'LAPORAN', 'POST-TEST', 'UTS', 'UAS', 'All']
ResetPasswordRequest = apps.get_model('assistant', 'ResetPasswordRequest')


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


class RequestPasswordResetForm(forms.ModelForm):
    class Meta:
        model = ResetPasswordRequest
        fields = ('user', )
