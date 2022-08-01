from .views import *
from django.urls import path

app_name = 'file'

urlpatterns = [
    path('', UploadFile.as_view(), name='upload'),
    path('my-files', MyFiles.as_view(), name='all-file')
]
