from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate
from .models import *
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *

# Create your views here.

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