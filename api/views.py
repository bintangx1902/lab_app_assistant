import datetime

import jwt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from django.contrib.auth import logout

def payloads(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed("auth failed, cause : ", e)

    return payload


def this_user(payload):
    return get_object_or_404(User, id=payload['user_id'])


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
        now = timezone.now()
        if now > get_qr.valid_until:
            return Response(data={'text': "Expired QR"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        """ find recap """
        recap = Recap.objects.filter(qr=get_qr, user=user)
        if recap:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'text': 'Anda Sudah Absen'})

        """ find if user in the class or not """
        if user not in get_qr.class_name.students.all():
            return Response(data={'text': 'Kamu Bukan Mahasiswa kelas ini !'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        instance = Recap(
            qr=get_qr,
            user=user
        )
        instance.save()

        return Response(data={'text': 'Berhasil di Recap'}, status=status.HTTP_202_ACCEPTED)


class LoginEndPoint(APIView):

    def get(self, format=None):
        token = self.request.COOKIES.get('jwt')
        if token:
            response = Response()
            response.data = {
                'jwt': token
            }
            return response
        return Response(status.HTTP_204_NO_CONTENT)

    def post(self, format=None):
        username = self.request.data.get("username")
        password = self.request.data.get('password')
        user = User.objects.filter(username=username).first()
        response = Response()

        if not user:
            raise AuthenticationFailed('User not found')

        # check if registered
        extended = hasattr(user, 'user')
        if not extended:
            response.data = {
                'text': "Mohon lengkapi data"
            }

        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            raise AuthenticationFailed("Password doesn't match")

        payload = {
            'user_id': user.id,
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response.data = {
            'jwt': token
        }
        return response


class AuthenticatedUser(APIView):
    def get(self, format=None):
        token = self.request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed("token missing")

        payload = payloads(token)
        user = this_user(payload)
        user_serializer = UserSerializer(user, many=False)
        profile_serializer = ProfileSerializer(user.user, many=False)
        student_serializer = ClassNameSerializer(user.stud.all(), many=True)
        assist_serializer = ClassNameSerializer(user.assist.all(), many=True)
        creator_serializer = ClassNameSerializer(user.class_creator.all(), many=True)

        return Response({
            "user": user_serializer.data,
            'profile': profile_serializer.data,
            'class_as_creator': creator_serializer.data,
            "class_as_student": student_serializer.data,
            'class_as_assistant': assist_serializer.data,
        })


class LogoutEndPoint(APIView):
    def get(self, format=None):
        token = self.request.META.get('HTTP_TOKEN')
        if token:
            data = {'jwt': token}
            return Response(data=data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, format=None):
        return self.logout(self.request)

    def logout(self, req):
        try:
            req.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist) as e:
            print(e)

        logout(req)

        return Response({'success': 'Successfully Logged out'}, status=status.HTTP_200_OK)
