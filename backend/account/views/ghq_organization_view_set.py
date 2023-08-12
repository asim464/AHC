from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from account.models import GHQOrganization
from account.serializers import GHQOrganizationSerializer
from account.decorator import route_permissions
from account.paginations import CustomPagination
from django_filters import rest_framework as filters
from account.filters import GHQOrganizationFilter


class GHQOrganizationViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = GHQOrganization.objects.exclude(name='Test Branch').order_by('id')
    serializer_class = GHQOrganizationSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GHQOrganizationFilter

    @route_permissions(['read_organization'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions(['read_organization'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
