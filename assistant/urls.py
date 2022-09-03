from .views import *
from django.urls import path

app_name = 'assist'

urlpatterns = [
    path('', AssistantLanding.as_view(), name='landing'),
    path('create-class', CreateClass.as_view(), name='create-class'),
    path('join-class', JoinAssistantClas.as_view(), name='join-class'),
    path('change-username', AssistantChangeUsername.as_view(), name='change-username'),
    path('change-password', AssistantChangePassword.as_view(), name='change-password'),
    path('my-class', MyClassList.as_view(), name='my-class-list'),
    path('my-class/<slug:link>/generate-qr', GenerateQRCodeView.as_view(), name='generate-qr'),
    path('my-class/<slug:link>/file/delete/<int:item_pk>', DeleteFile.as_view(), name='delete-file'),
    path('my-class/<slug:link>/file/<name>', QRCodeView.as_view(), name='view-qr'),
    path('my-class/<slug:link>/file', SeeAllFiles.as_view(), name='file-class'),
    path('my-class/<slug:link>/recaps/<qr_code>', PresenceRecap.as_view(), name='recaps'),
    path('my-class/<slug:link>/recaps', QRGeneratedList.as_view(), name='generated-qr'),
    path('my-class/<slug:link>', MyClass.as_view(), name='my-class'),
]
