from .views import *
from django.urls import path

app_name = 'assist'

urlpatterns = [
    path('', AssistantLanding.as_view(), name='landing'),
    path('file-view', SeeAllFiles.as_view(), name='files'),
    path('create-class', create_class, name='create-class'),
    path('backup-option', backup, name='backup'),
    path('my-class', MyClassList.as_view(), name='my-class-list'),
    path('my-class/<slug:link>/generate-qr', GenerateQRCodeView.as_view(), name='generate-qr'),
    path('my-class/<slug:link>', MyClass.as_view(), name='my-class'),
]
