from rest_framework import serializers
from api.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    parent_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organization
        fields = (
            'id', 'name', 'parent', 'description', 'organization_type', 'is_delete', 'insert_date', 'insert_by',
            'update_date', 'update_by', 'location', 'datacenter_id', 'username_prefix', 'signal_center_id',
            'arm_type', 'ams_type', 'online_status', 'org_code', 'org_status', 'city_code',
            'parent_data'
        )
        read_only_fields = (
            'id', 'name', 'parent', 'description', 'organization_type', 'is_delete', 'insert_date', 'insert_by',
            'update_date', 'update_by', 'location', 'datacenter_id', 'username_prefix', 'signal_center_id',
            'arm_type', 'ams_type', 'online_status', 'org_code', 'org_status', 'city_code', 'parent_data'
        )

    def get_parent_data(self, obj):
        if not obj.parent:
            return None

        organization = Organization.objects.get(pk=obj.parent.id)
        data = {
            'id': organization.id,
            'name': organization.name,
        }
        return data
