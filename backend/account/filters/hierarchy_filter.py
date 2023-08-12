import django_filters as filters
from account.models import Hierarchy


class HierarchyFilter(filters.FilterSet):
    parent_name = filters.CharFilter(field_name='parent__name', lookup_expr='icontains')
    child_name = filters.CharFilter(field_name='child__name', lookup_expr='icontains')

    class Meta:
        model = Hierarchy
        fields = [
            'parent_name',
            'child_name'
        ]
