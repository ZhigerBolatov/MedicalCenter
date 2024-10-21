from django.contrib.auth import login, authenticate
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import *
from .models import *
from .tasks import *

import os
from datetime import timedelta
from django.utils import timezone


class AuthenticationAPIView(APIView):
    permission_classes = []

    def post(self, request):
        happylogin = request.data.get('happylogin')
        happypassword = request.data.get('happypassword')
        user = HappyLifeUsers.object.filter(Q(IIN=happylogin) | Q(email=happylogin) | Q(telephone=happylogin))

        if not user:
            return Response(data={'found': False, 'password': False}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(IIN=user[0].IIN, password=happypassword)

        if user is None:
            return Response(data={'found': True, 'password': False}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response(data={'found': True, 'password': True}, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)


class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = HappyLifeUsers.object.filter(email=email).first()
        if user:
            random_token = os.urandom(32).hex()
            reset_password_token = ResetPasswordToken(user=user, token=random_token)
            reset_password_token.save()
            message = (f"User on happylifes.org requested a reset password. "
                       f"If it was not you, please ignore this mail\n\n"
                       f"Your reset token: {random_token}\n\n"
                       f"Generation Time: {reset_password_token.created_at}\n"
                       f"You have 10 minutes to use this token, otherwise it would be bot valid!")
            send_notification_mail(email, message)
            return Response(data={'success': True}, status=status.HTTP_200_OK)
        return Response(data={'success': False}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = HappyLifeUsers.object.filter(email=email).first()
        if user:
            token = request.data.get('token')
            reset_password_token = ResetPasswordToken.objects.filter(Q(user=user) & Q(token=token)).first()
            if not reset_password_token:
                return Response(data={'success': False,
                                      'message': 'Email and/or Token is not valid!'},
                                status=status.HTTP_400_BAD_REQUEST)

            if timezone.now() - reset_password_token.created_at > timedelta(minutes=10):
                return Response(data={'success': False,
                                      'message': 'Token was expired!'},
                                status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            reset_password_token.delete()
            return Response(data={'success': True,
                                  'message': 'Password successfully updated!'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'success': False,
                              'message': 'Email and/or Token is not valid!'},
                        status=status.HTTP_400_BAD_REQUEST)
