from app.models.user import User
from rest_framework import permissions, generics, filters
from app.serializers.user import (UserSerializer, LogInSerializer,
                                        RegisterSerializer,
                                        RefreshTokenSerializer,
                                        ResetPasswordSerializer)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from dj_rest_auth.views import PasswordResetView
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class SignUpAPI(generics.CreateAPIView):
    """Takes a set of user credentials and creates an account"""
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = RegisterSerializer
    queryset = User.objects


class LoginView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.

    Sample Response:

            {
                refresh_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                                eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MTg3MTI2NywiaWF0IjoxNjYxNzg0ODY3LCJqdGkiOiI0MzYyNWJmM2I4ZDc0ZTEyYjFkNWYxNTJiZmVlOTViYSIsInVzZXJfaWQiOjR9.gyugLEMBTO-HFmKl8fWI9SBK8AKdPLwMjatRiEYwXxs",
                access_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                                eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MTg3MTI2NywiaWF0IjoxNjYxNzg0ODY3LCJqdGkiOiI0MzYyNWJmM2I4ZDc0ZTEyYjFkNWYxNTJiZmVlOTViYSIsInVzZXJfaWQiOjR9.gyugLEMBTO-HFmKl8fWI9SBK8AKdPLwMjatRiEYwXxs"
            }
    """
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = LogInSerializer


class RefreshTokenView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.

    Sample Response:

            {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                                eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxODcxNDI5LCJpYXQiOjE2NjE3ODQ4NjcsImp0aSI6IjNhMjIyODEwNDQ3ZTQ4ODg4OTMzNjkwYmFlOWViOTMyIiwidXNlcl9pZCI6NH0.13ec7VYKPRL-upWlwdprmUOw0p-ssC6cMPxAqoDi310"
            }
    """
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = RefreshTokenSerializer


class RetrieveUserAPI(generics.RetrieveAPIView):
    """Returns details of a user"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    lookup_field = "id"
    queryset = User.objects


class ListUserAPI(generics.ListAPIView):
    """Returns details of all users"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer
    queryset = User.objects.order_by('id')
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = ['is_deleted', 'last_name', 'first_name', 'role']
    search_fields = ['first_name', 'last_name', 'role', 'email']


class DeleteUserAPI(generics.DestroyAPIView):
    """Delete User by id"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects
    lookup_field = 'id'


class UpdateUserAPI(generics.UpdateAPIView):
    """Updates user details"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisterSerializer
    queryset = User.objects
    lookup_field = 'id'


class ResetPasswordView(PasswordResetView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]
