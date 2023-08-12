from rest_framework import serializers
from account.models import GHQOrganization


class GHQOrganizationSerializer(serializers.ModelSerializer):
    parent_data = serializers.SerializerMethodField(read_only=True)
    children_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GHQOrganization
        fields = (
            'id', 'name', 'parent', 'description', 'organization_type', 'is_delete', 'insert_date', 'insert_by',
            'update_date', 'update_by', 'location', 'datacenter_id', 'username_prefix', 'signal_center_id',
            'arm_type', 'ams_type', 'online_status', 'org_code', 'org_status', 'city_code',
            'parent_data', 'children_data', 'children',
        )
        read_only_fields = (
            'id', 'name', 'parent', 'description', 'organization_type', 'is_delete', 'insert_date', 'insert_by',
            'update_date', 'update_by', 'location', 'datacenter_id', 'username_prefix', 'signal_center_id',
            'arm_type', 'ams_type', 'online_status', 'org_code', 'org_status', 'city_code', 'parent_data','children_data'
        )

    def get_parent_data(self, obj):
        if not obj.parent:
            return None

        organization = GHQOrganization.objects.get(pk=obj.parent.id)
        data = {
            'id': organization.id,
            'name': organization.name,
        }
        return data

    def get_children_data(self, obj):
        children = obj.children.all()
        if len(children) > 0:
            data = []
            for child in children:
                data.append({
                    'id': child.child.id,
                    'name': child.child.name
                })
            if len(data) == 0:
                return None
            return data
        else:
            return None
