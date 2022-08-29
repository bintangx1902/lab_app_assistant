from .views import *
from django.urls import path

app_name = 'presence'

urlpatterns = [
    path('join-class', JoinClass.as_view(), name='join-class'),
    path('data-completions', DataComplement.as_view(), name='complete-data'),
    path('class-list', ClassList.as_view(), name='class-list'),
    path('presence', Presence.as_view(), name='take-presence'),
    path('class/<slug:link>/upload-file', UploadFileByClass.as_view(), name='upload-file'),
    path('class/<slug:link>/file-list', FileListClass.as_view(), name='file-list-class'),
    path('', LandingView.as_view(), name='landing'),
]
