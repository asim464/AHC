from rest_framework import serializers
from account.models import GHQUser, GHQOrganization
from api.models import User, Role


class GHQUserSerializer(serializers.ModelSerializer):
    role_data = serializers.SerializerMethodField(read_only=True)
    organization_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GHQUser
        fields = (
            'id', 'username', 'name', 'password', 'profile_status', 'telephone', 'svc_number', 'is_delete', 'rank_name',
            'service_name', 'rank_order', 'rank_id', 'appointment_id', 'appointment_name', 'appointment_order',
            'executive_order', 'appointment_type', 'data_center_id', 'profile_image', 'organization', 'role_data',
            'organization_data'
        )

        read_only_fields = (
            'id', 'username', 'name', 'profile_status', 'telephone', 'svc_number', 'is_delete', 'rank_name',
            'service_name', 'rank_order', 'rank_id', 'appointment_id', 'appointment_name', 'appointment_order',
            'executive_order', 'appointment_type', 'data_center_id', 'organization', 'role_data', 'organization_data'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_role_data(self, obj):
        try:
            user = User.objects.get(pk=obj.pk)
            if not user.role:
                return None

            role = Role.objects.get(pk=user.role.id)
            data = {
                'id': role.id,
                'name': role.name,
                'code_name': role.code_name
            }

            return data
        except User.DoesNotExist:
            return None

    def get_organization_data(self, obj):
        if not obj.organization:
            return None

        organization = GHQOrganization.objects.get(pk=obj.organization.id)
        data = {
            'id': organization.id,
            'name': organization.name,
        }
        return data
