from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import GHQUser
from api.models import User
from api.util import ldap_authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get("password", None)

        if not username or not password:
            raise serializers.ValidationError({'msg': 'Invalid data.'})

        # if not ldap_authenticate(username=username, password=password):
        #     raise serializers.ValidationError({'msg': 'Invalid credentials.'})

        # ghq_users = GHQUser.objects.filter(username=username).order_by('appointment_order').all()
        # if len(ghq_users) == 0:
        #     raise serializers.ValidationError({'msg': 'User does not exists.'})
        # ghq_user = ghq_users[0]

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'msg': 'Invalid credentials.'})

        attrs['user'] = user
        # attrs['ghq_user'] = ghq_user
        return attrs
