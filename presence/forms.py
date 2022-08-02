from django import forms
from .models import *


class UserCompletionForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserDataCompleteForms(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['nim', 'phone_number']
