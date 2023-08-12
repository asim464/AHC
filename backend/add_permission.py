import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ahc.settings')

import django

django.setup()

from api.models import Permission

permissions = [
    Permission(name='Create Role', code_name='create_role', module_name='Role', description='User can create role'),
    Permission(name='Read Role', code_name='read_role', module_name='Role', description='User can read role'),
    Permission(name='Update Role', code_name='update_role', module_name='Role', description='User can update role'),
    Permission(name='Delete Role', code_name='delete_role', module_name='Role', description='User can delete role'),
    Permission(name='Show Role', code_name='show_role', module_name='Role', description='User can show role'),
    Permission(name='Create User', code_name='create_user', module_name='User', description='User can create user'),
    Permission(name='Update User', code_name='update_user', module_name='User', description='User can update user'),
    Permission(name='Read User', code_name='read_user', module_name='User', description='User can read user'),
    Permission(name='Show User', code_name='show_user', module_name='User', description='User can show user'),
    Permission(name='Read Organization', code_name='read_organization', module_name='Organization',
               description='User can read organization'),
    Permission(name='Show Organization', code_name='show_organization', module_name='Organization',
               description='User can show organization'),

    Permission(name='Create Complaint Type', code_name='complaint_type_create', module_name='Complaint Type',
               description='User can create Complaint Type'),
    Permission(name='Read Complaint Type', code_name='complaint_type_read', module_name='Complaint Type',
               description='User can read Complaint Type'),
    Permission(name='Update Complaint Type', code_name='complaint_type_update', module_name='Complaint Type',
               description='User can update Complaint Type'),
    Permission(name='Delete Complaint Type', code_name='complaint_type_delete', module_name='Complaint Type',
               description='User can delete Complaint Type'),
    Permission(name='Show Complaint Type', code_name='complaint_type_show', module_name='Complaint Type',
               description='User can show Complaint Type'),

    Permission(name='Create Martial Status', code_name='martial_status_create', module_name='Martial Status',
               description='User can create Martial Status'),
    Permission(name='Read Martial Status', code_name='martial_status_read', module_name='Martial Status',
               description='User can read Martial Status'),
    Permission(name='Update Martial Status', code_name='martial_status_update', module_name='Martial Status',
               description='User can update Martial Status'),
    Permission(name='Delete Martial Status', code_name='martial_status_delete', module_name='Martial Status',
               description='User can delete Martial Status'),
    Permission(name='Show Martial Status', code_name='martial_status_show', module_name='Martial Status',
               description='User can show Martial Status'),

Permission(name='Create Corps', code_name='corps_create', module_name='Corps',
               description='User can create Corps'),
    Permission(name='Read Corps', code_name='corps_read', module_name='Corps',
               description='User can read Corps'),
    Permission(name='Update Corps', code_name='corps_update', module_name='Corps',
               description='User can update Corps'),
    Permission(name='Delete Corps', code_name='corps_delete', module_name='Corps',
               description='User can delete Corps'),
    Permission(name='Show Corps', code_name='corps_show', module_name='Corps',
               description='User can show Corps'),


Permission(name='Create Serving Serving', code_name='serving_status_create', module_name='Serving Status',
               description='User can create Serving Status'),
    Permission(name='Read Serving Status', code_name='serving_status_read', module_name='Serving Status',
               description='User can read Serving Status'),
    Permission(name='Update Serving Status', code_name='serving_status_update', module_name='Serving Status',
               description='User can update Serving Status'),
    Permission(name='Delete Serving Status', code_name='serving_status_delete', module_name='Serving Status',
               description='User can delete Serving Status'),
    Permission(name='Show Serving Status', code_name='serving_status_show', module_name='Serving Status',
               description='User can show Serving Status'),

Permission(name='Create City', code_name='city_create', module_name='City',
               description='User can create City'),
    Permission(name='Read City', code_name='city_read', module_name='City',
               description='User can read City'),
    Permission(name='Update City', code_name='city_update', module_name='City',
               description='User can update City'),
    Permission(name='Delete City', code_name='city_delete', module_name='City',
               description='User can delete City'),
    Permission(name='Show City', code_name='city_show', module_name='City',
               description='User can show City'),

Permission(name='Create Category', code_name='category_create', module_name='Category',
               description='User can create Category'),
    Permission(name='Read Category', code_name='category_read', module_name='Category',
               description='User can read Category'),
    Permission(name='Update Category', code_name='category_update', module_name='Category',
               description='User can update Category'),
    Permission(name='Delete Category', code_name='category_delete', module_name='Category',
               description='User can delete Category'),
    Permission(name='Show Category', code_name='category_show', module_name='Category',
               description='User can show Category'),

]


def add_permission():
    for permission in permissions:
        try:
            Permission.objects.get(code_name=permission.code_name)
        except Permission.DoesNotExist:
            permission.save()


if __name__ == '__main__':
    print("Adding permissions to AHC...")
    add_permission()
