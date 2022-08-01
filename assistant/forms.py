from django.apps import apps
from django.forms import ModelForm

Files = apps.get_model('file_control', 'Files')
Recap = apps.get_model('presence', 'Recap')
ClassName = apps.get_model('presence', 'ClassName')
GenerateQRCode = apps.get_model('presence', 'GenerateQRCode')
UserData = apps.get_model('presence', 'UserData')


class ClassCreationForms(ModelForm):
    class Meta:
        model = ClassName
        fields = '__all__'
