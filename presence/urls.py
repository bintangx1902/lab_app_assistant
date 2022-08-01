from .views import *
from django.urls import path

app_name = 'presence'

urlpatterns = [
    path('join-class', join_class, name='join-class'),
]
