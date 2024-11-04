from rest_framework.serializers import ModelSerializer
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = HappyLifeUsers
        fields = ['id', 'IIN', 'first_name', 'last_name', 'role_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['role'] = instance.role_id.name
        return representation
