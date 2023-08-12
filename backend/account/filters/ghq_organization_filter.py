import django_filters as filters
from account.models import GHQOrganization


class GHQOrganizationFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    parent = filters.NumberFilter(field_name='parent')

    class Meta:
        model = GHQOrganization
        fields = [
            'name',
            'parent'
        ]
