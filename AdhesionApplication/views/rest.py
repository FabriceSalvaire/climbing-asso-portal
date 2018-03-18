####################################################################################################

# from account.conf import settings
# settings.AUTH_USER_MODEL
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions

from ..serializers import (
    UserSerializer,
    UserProfileSerializer,
)

from ..models import (
    UserProfile,
)

####################################################################################################

class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

####################################################################################################

class UserProfileViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAdminUser,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
