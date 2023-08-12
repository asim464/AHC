from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from account.models import GHQUser
from account.serializers import GHQUserSerializer
from account.decorator import route_permissions
from account.paginations import CustomPagination
from django_filters import rest_framework as filters
from account.filters import GHQUserFilter


class GHQUserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = GHQUser.objects.exclude(username='superuser').order_by('appointment_order')
    serializer_class = GHQUserSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GHQUserFilter

    @route_permissions(['read_user'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions(['read_user'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
