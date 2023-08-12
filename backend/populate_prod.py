import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ahc.settings')

import django

django.setup()

from api.models import User, Permission, Role, Organization
from account.models import GHQUser, GHQOrganization


def populate():
    permissions = Permission.objects.all()

    try:
        role = Role.objects.get(code_name='su')
        role.permissions.clear()
    except Role.DoesNotExist:
        role = Role.objects.create(name='SuperUser', code_name='su')

    role.permissions.add(*permissions)
    role.save()

    try:
        user = User.objects.get(username='superuser')
    except User.DoesNotExist:
        user = User.objects.create_superuser(
            id=1,
            username="superuser",
            password="123",
        )
        user.name = 'Superuser'
        user.role = Role.objects.get(code_name='su')
        organization = GHQOrganization.objects.get(name='Test Branch')
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
        user.organization_id = Organization.objects.get(name='Test Branch')
        user.appointment_id = GHQUser.objects.get(username='superuser').appointment_id
        user.save()


if __name__ == '__main__':
    print("Starting AHC population script...")
    populate()
