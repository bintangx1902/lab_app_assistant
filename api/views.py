from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from rest_framework import status
from django.contrib.auth.models import User

Recap = apps.get_model('presence', 'Recap')
ClassName = apps.get_model('presence', 'ClassName')
GenerateQRCode = apps.get_model('presence', 'GenerateQRCode')


class TakePresenceEndPoint(APIView):
    def get(self, *args, **kwargs):
        return Response()

    def post(self, *args, **kwargs):
        code = self.request.data.get('code')
        user_id = int(self.request.data.get('unknown_number'))
        get_qr = GenerateQRCode.objects.filter(qr_code=code)
        user = User.objects.filter(id=user_id)
        if not get_qr:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'text': 'qr not found'})
        if not user:
            return Response(data={'text': 'number is unknown'}, status=status.HTTP_404_NOT_FOUND)
        user = user[0]
        get_qr = get_qr[0]

        """ find recap """
        recap = Recap.objects.filter(qr=get_qr, user=user)
        if recap:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'text': 'Anda Sudah Absen'})

        instance = Recap(
            qr=get_qr,
            user=user
        )
        instance.save()
        instance.save(using='backup')

        return Response({'say': 'hai'})
