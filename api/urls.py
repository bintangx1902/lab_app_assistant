from django.urls import path
from .views import TakePresenceEndPoint

app_name = 'api'


urlpatterns = [
    path('take-presence', TakePresenceEndPoint.as_view(), name='take-presence')
]
