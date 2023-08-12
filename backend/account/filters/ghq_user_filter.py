import django_filters as filters
from account.models import GHQUser


class GHQUserFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    username = filters.CharFilter(field_name='username', lookup_expr='contains')
    organization = filters.NumberFilter(field_name='organization__id')

    class Meta:
        model = GHQUser
        fields = [
            'name',
            'username',
            'organization'
        ]
