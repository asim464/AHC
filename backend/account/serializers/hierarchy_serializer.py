from rest_framework import serializers
from account.models import Hierarchy, GHQOrganization, GHQUser


class HierarchySerializer(serializers.ModelSerializer):
    parent_data = serializers.SerializerMethodField(read_only=True)
    child_data = serializers.SerializerMethodField(read_only=True)
    created_by_data = serializers.SerializerMethodField(read_only=True)
    updated_by_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Hierarchy
        fields = (
            'id', 'level', 'parent', 'child', 'created_at', 'created_by', 'updated_at', 'updated_by', 'parent_data',
            'child_data', 'created_by_data', 'updated_by_data'
        )
        read_only_fields = ('parent_data', 'child_data', 'created_by_data', 'updated_by_data')

    def create(self, validated_data):
        if Hierarchy.objects.filter(parent=validated_data['parent'], child=validated_data['child']).exists():
            raise serializers.ValidationError({"msg": "Parent child relationship already exists"})

        organization_child = Hierarchy.objects.create(**validated_data)
        return organization_child

    def update(self, instance, validated_data):
        if instance.parent != validated_data['parent'] or instance.child != validated_data['child']:
            if Hierarchy.objects.filter(parent=validated_data['parent'], child=validated_data['child']).exists():
                raise serializers.ValidationError({"msg": "Parent child relationship already exists"})

        instance.child = validated_data.get('child', instance.child)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.level = validated_data.get('level', instance.level)

        instance.save()
        return instance

    def get_parent_data(self, obj):
        if not obj.parent:
            return None

        organization = GHQOrganization.objects.get(pk=obj.parent.id)
        data = {
            'id': organization.id,
            'name': organization.name,
        }
        return data

    def get_child_data(self, obj):
        if not obj.child:
            return None

        organization = GHQOrganization.objects.get(pk=obj.child.id)
        data = {
            'id': organization.id,
            'name': organization.name,
        }
        return data

    def get_created_by_data(self, obj):
        if not obj.created_by:
            return None

        user = GHQUser.objects.get(pk=obj.created_by.id)
        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
        }
        return data

    def get_updated_by_data(self, obj):
        if not obj.updated_by:
            return None

        user = GHQUser.objects.get(pk=obj.updated_by.id)
        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
        }
        return data
