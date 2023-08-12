from django.db import models
from account.models import Hierarchy


class Organization(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    organization_type = models.CharField(max_length=255, blank=True, null=True)
    is_delete = models.CharField(max_length=255, blank=True, null=True)
    insert_date = models.DateTimeField(blank=True, null=True)
    insert_by = models.CharField(max_length=255, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_by = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    datacenter_id = models.BigIntegerField(blank=True, null=True)
    username_prefix = models.CharField(max_length=255, blank=True, null=True)
    signal_center_id = models.BigIntegerField(blank=True, null=True)
    arm_type = models.BigIntegerField(blank=True, null=True)
    ams_type = models.BigIntegerField(blank=True, null=True)
    online_status = models.CharField(max_length=255, blank=True, null=True)
    org_code = models.BigIntegerField(blank=True, null=True)
    org_status = models.CharField(max_length=255, blank=True, null=True)
    city_code = models.BigIntegerField(blank=True, null=True)
    parent = models.ForeignKey('Organization', related_name='+', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_children(self, level=None, include_self=False):
        children = []
        if level:
            hierarchies = Hierarchy.objects.filter(parent__id=self.id, level=level).all()
        else:
            hierarchies = Hierarchy.objects.filter(parent__id=self.id).all()

        for hierarchy in hierarchies:
            child = hierarchy.child
            Organization.add_organizations(organization=child)
            children.append(Organization.objects.get(pk=child.id))

        if include_self:
            children.append(self)
        return children

    @staticmethod
    def add_organizations(organization):
        if organization.parent is None:
            Organization.objects.get_or_create(
                id=organization.id,
                name=organization.name,
                description=organization.description,
                organization_type=organization.organization_type,
                is_delete=organization.is_delete,
                insert_date=organization.insert_date,
                insert_by=organization.insert_by,
                update_date=organization.update_date,
                update_by=organization.update_by,
                location=organization.location,
                datacenter_id=organization.datacenter_id,
                username_prefix=organization.username_prefix,
                signal_center_id=organization.signal_center_id,
                arm_type=organization.arm_type,
                ams_type=organization.ams_type,
                online_status=organization.online_status,
                org_code=organization.org_code,
                parent=organization.parent,
            )
        else:
            Organization.add_organizations(organization.parent)
            Organization.objects.get_or_create(
                id=organization.id,
                name=organization.name,
                description=organization.description,
                organization_type=organization.organization_type,
                is_delete=organization.is_delete,
                insert_date=organization.insert_date,
                insert_by=organization.insert_by,
                update_date=organization.update_date,
                update_by=organization.update_by,
                location=organization.location,
                datacenter_id=organization.datacenter_id,
                username_prefix=organization.username_prefix,
                signal_center_id=organization.signal_center_id,
                arm_type=organization.arm_type,
                ams_type=organization.ams_type,
                online_status=organization.online_status,
                org_code=organization.org_code,
                parent=Organization.objects.get(pk=organization.parent.id),
            )
