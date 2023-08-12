from rest_framework import serializers
from api.models import MartialStatus, User


class MartialStatusSerializer(serializers.ModelSerializer):
    created_by_data = serializers.SerializerMethodField(read_only=True)
    updated_by_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MartialStatus
        fields = ('id', 'name', 'created_at', 'updated_at', 'created_by', 'created_by_data', 'updated_by', 'updated_by_data')
        read_only_fields = ('created_at', 'created_by_data', 'updated_at', 'updated_by_data')

    def get_created_by_data(self, obj):
        if not obj.created_by:
            return None

        user = User.objects.get(pk=obj.created_by.id)
        data = {
            'name': user.name,
            'username': user.username,
            'organization': user.organization.name,
            'appointment': user.appointment_name,
        }
        return data

    def get_updated_by_data(self, obj):
        if not obj.updated_by:
            return None

        user = User.objects.get(pk=obj.updated_by.id)
        data = {
            'name': user.name,
            'username': user.username,
            'organization': user.organization.name,
            'appointment': user.appointment_name,
        }
        return data
