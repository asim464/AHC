from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import Corps
from api.serializers import CorpsSerializer
from api.decorator import route_permissions
from api.paginations import CustomPagination


class CorpsViewSet(viewsets.ModelViewSet):
    queryset = Corps.objects.order_by('id')
    serializer_class = CorpsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    @route_permissions(['corps_read'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions(['corps_create'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions(['corps_read'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions(['corps_update'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions(['corps_update'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions(['corps_delete'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)