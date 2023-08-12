from django.middleware import csrf
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.util import set_access_cookies, set_refresh_cookies, get_tokens_for_user, combine_role_permissions
from api.serializers import UserSerializer, LoginSerializer


class LoginView(APIView):

    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        response = Response()

        token = get_tokens_for_user(user)
        set_access_cookies(response, token['access'])
        set_refresh_cookies(response, token['refresh'])
        csrf.get_token(request)

        data = UserSerializer(user, context={'request': request}).data
        data['permissions'] = combine_role_permissions(user.role)

        response.status_code = status.HTTP_200_OK
        response.data = {"msg": "Login successfully", "user": data}

        return response
