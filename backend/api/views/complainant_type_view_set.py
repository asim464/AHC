from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import ComplainantType
from api.serializers import ComplainantTypeSerializer
from api.decorator import route_permissions
from api.paginations import CustomPagination


class ComplainantTypeViewSet(viewsets.ModelViewSet):
    queryset = ComplainantType.objects.order_by('id')
    serializer_class = ComplainantTypeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    @route_permissions(['complaint_type_read'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions(['complaint_type_create'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions(['complaint_type_read'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions(['complaint_type_update'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions(['complaint_type_update'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions(['complaint_type_delete'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)