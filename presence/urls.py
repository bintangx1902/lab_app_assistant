from .views import *
from django.urls import path

app_name = 'presence'

urlpatterns = [
    path('join-class', JoinClass.as_view(), name='join-class'),
    path('data-completions', DataComplement.as_view(), name='complete-data'),
    path('reset-password/request', RequestPasswordReset.as_view(), name='request-password-reset'),
    path('reset-password/<token>', ResetPassword.as_view(), name='reset-password'),
    path('presence', Presence.as_view(), name='take-presence'),
    path('class', ClassList.as_view(), name='class-list'),
    path('class/<slug:link>/upload-file', UploadFileByClass.as_view(), name='upload-file'),
    path('class/<slug:link>/file-list', FileListClass.as_view(), name='file-list-class'),
    path('class/<slug:link>/recaps', MyPresenceRecaps.as_view(), name='my-presence-recap'),
    path('class/<slug:link>/recaps/score', SeeMyScoreView.as_view(), name='my-score-recap'),
    path('', LandingView.as_view(), name='landing'),
]
