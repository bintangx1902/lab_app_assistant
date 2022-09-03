from django.apps import apps
from django.forms import ModelForm, DateTimeInput
from django.contrib.auth.models import User

Files = apps.get_model('file_control', 'Files')
Recap = apps.get_model('presence', 'Recap')
ClassName = apps.get_model('presence', 'ClassName')
GenerateQRCode = apps.get_model('presence', 'GenerateQRCode')
UserData = apps.get_model('presence', 'UserData')


class ClassCreationForms(ModelForm):
    class Meta:
        model = ClassName
        fields = '__all__'


class GenerateQRCodeForms(ModelForm):
    class Meta:
        model = GenerateQRCode
        fields = ['valid_until']

        widgets = {
            'valid_until': DateTimeInput(attrs={'type': 'datetime-local'})
        }


class UserChangeDataForms(ModelForm):
    class Meta:
        model = User
        fields = ['username']


class CreateClassForms(ModelForm):
    class Meta:
        model = ClassName
        fields = ["lecture_name"]
