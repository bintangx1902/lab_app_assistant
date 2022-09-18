from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('take-presence', TakePresenceEndPoint.as_view(), name='take-presence'),
    path('login', LoginEndPoint.as_view(), name='login'),
    path('logout', LogoutEndPoint.as_view(), name='logout'),
    path('auth-user', AuthenticatedUser.as_view(), name='auth-user'),
]
