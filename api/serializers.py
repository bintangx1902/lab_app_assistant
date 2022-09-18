from django.apps import apps
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

ClassName = apps.get_model('presence', 'ClassName')
Recap = apps.get_model('presence', 'Recap')
GenerateQRCode = apps.get_model('presence', 'GenerateQRCode')
UserData = apps.get_model('presence', 'UserData')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'


class ClassNameSerializer(ModelSerializer):
    class Meta:
        model = ClassName
        fields = '__all__'

