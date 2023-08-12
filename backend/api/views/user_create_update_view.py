from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import GHQOrganization
from api.models import User, Organization, Role


class UserCreateUpdateView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data

        Organization.add_organizations(GHQOrganization.objects.get(pk=data['organization']))

        try:
            user = User.objects.get(pk=data['id'])
            user.username = data['username']
            user.name = data['name']
            user.profile_status = data['profile_status']
            user.telephone = data['telephone']
            user.rank_name = data['rank_name']
            user.service_name = data['service_name']
            user.rank_order = data['rank_order']
            user.rank_id = data['rank_id']
            user.appointment_id = data['appointment_id']
            user.appointment_name = data['appointment_name']
            user.appointment_order = data['appointment_order']
            user.executive_order = data['executive_order']
            user.appointment_type = data['appointment_type']
            user.data_center_id = data['data_center_id']
            user.organization = Organization.objects.get(pk=data['organization'])
            if data['role']:
                user.role = Role.objects.get(pk=data['role'])
            else:
                user.role = None
            user.save()
        except User.DoesNotExist:
            role = None
            if data['role']:
                role = Role.objects.get(pk=data['role'])

            User.objects.create(
                id=data['id'],
                username=data['username'],
                name=data['name'],
                profile_status=data['profile_status'],
                telephone=data['telephone'],
                rank_name=data['rank_name'],
                service_name=data['service_name'],
                rank_order=data['rank_order'],
                rank_id=data['rank_id'],
                appointment_id=data['appointment_id'],
                appointment_name=data['appointment_name'],
                appointment_order=data['appointment_order'],
                executive_order=data['executive_order'],
                appointment_type=data['appointment_type'],
                data_center_id=data['data_center_id'],
                organization=Organization.objects.get(pk=data['organization']),
                role=role
            )

        response = Response()

        response.status_code = status.HTTP_200_OK
        response.data = {"msg": "User updated successfully"}

        return response
