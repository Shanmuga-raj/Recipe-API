"""
Views for User API.
"""
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(CreateAPIView):
    """Create a New User."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    "Create a new auth Token for User."
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user
