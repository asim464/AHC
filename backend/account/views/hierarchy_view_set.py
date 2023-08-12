from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from account.models import Hierarchy
from account.serializers import HierarchySerializer
from account.decorator import route_permissions
from account.paginations import CustomPagination
from rest_framework import status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from account.filters import HierarchyFilter


class HierarchyViewSet(viewsets.ModelViewSet):
    queryset = Hierarchy.objects.order_by('id')
    serializer_class = HierarchySerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HierarchyFilter

    @route_permissions(['read_hierarchy'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions(['create_hierarchy'])
    def create(self, request, *args, **kwargs):
        serializer = HierarchySerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @route_permissions(['read_hierarchy'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions(['update_hierarchy'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions(['update_hierarchy'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions(['delete_hierarchy'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
