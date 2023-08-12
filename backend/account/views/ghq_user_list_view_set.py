from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from account.filters import GHQUserFilter
from account.models import GHQUser
from account.decorator import route_permissions
from account.serializers import GHQUserSerializer


class GHQUserListViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GHQUserSerializer
    queryset = GHQUser.objects.exclude(username='superuser').order_by('appointment_order')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GHQUserFilter

    @route_permissions(['read_user'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
