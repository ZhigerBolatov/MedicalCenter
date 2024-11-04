from django.contrib.auth import login, authenticate, logout
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
            return Response(data={'success': False}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(IIN=user[0].IIN, password=happypassword)

        if user is None:
            return Response(data={'success': False}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        try:
            role = user.role_id.name
        except AttributeError:
            role = None
        return Response(data={'success': True, 'role': role}, status=status.HTTP_200_OK)


class LogOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(data={'success': True}, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = HappyLifeUsers.object.get(email='123@gmail.com')
        data = UserSerializer(user, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)


class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = HappyLifeUsers.object.filter(email=email).first()
        if user:
            random_token = os.urandom(3).hex()[:6] 
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


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        iin = request.data.get('iin')
        user_check = HappyLifeUsers.object.filter(IIN=iin)
        if user_check:
            return Response(data={'success': False,
                                  'message': 'User with this IIN already exists!'},
                            status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        user_check = HappyLifeUsers.object.filter(email=email)
        if user_check:
            return Response(data={'success': False,
                                  'message': 'User with this email already exists!'},
                            status=status.HTTP_400_BAD_REQUEST)

        telephone = request.data.get('telephone')
        user_check = HappyLifeUsers.object.filter(telephone=telephone)
        if user_check:
            return Response(data={'success': False,
                                  'message': 'User with this telephone already exists!'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(name='Patients')
        except Role.DoesNotExist:
            return Response(data={'success': False,
                                  'message': 'Role \'Patients\' does not exist! You have to create it!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        password = request.data.get('password')
        extra_fields = {
            'last_name': request.data.get('last_name'),
            'first_name': request.data.get('first_name'),
            'telephone': telephone,
            'user_address': request.data.get('user_address'),
            'email': email,
            'role_id': role
        }
        user = HappyLifeUsers.object.create_user(IIN=iin, password=password, **extra_fields)
        return Response(data={'success': True,
                              'message': 'User successfully created!'},
                        status=status.HTTP_201_CREATED)


class AuthInfoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            role = request.user.role_id.name
            return Response(data={'is_authenticated': True,
                                  'role': role},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={'is_authenticated': False}, status=status.HTTP_200_OK)
