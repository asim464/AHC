from django.db import models


class GHQOrganization(models.Model):
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
    parent = models.ForeignKey('GHQOrganization', related_name='+', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_children(self, level=None, include_self=False):
        children = []
        if level:
            organization_children = self.children.filter(level=level).all()
        else:
            organization_children = self.children.all()
        for organization_child in organization_children:
            children.append(organization_child.child)
        if include_self:
            children.append(self)
        return children
