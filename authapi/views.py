"""
Views for User API.
"""
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """Create a New User."""

    serializer_class = UserSerializer
