from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import City
from api.serializers import CitySerializer
from api.decorator import route_permissions
from api.paginations import CustomPagination


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.order_by('id')
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    @route_permissions(['city_read'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions(['city_create'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions(['city_read'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions(['city_update'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions(['city_update'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions(['city_delete'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)