from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = HappyLifeUsers
        fields = ['id', 'first_name', 'last_name','role_id']