from django import forms
from .models import Files


class FileUploadForms(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file']
