"""
Accounts API Views - Profile and user API endpoints.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile CRUD.

    Endpoints:
    - GET /accounts/api/v1/profiles/ - List profiles (admin only)
    - GET /accounts/api/v1/profiles/{id}/ - Profile detail
    - GET /accounts/api/v1/profiles/me/ - Current user's profile
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        """
        Return permission classes based on action.

        Admin-only access for list and destroy actions.
        Authenticated access for other actions (retrieve, update, me).

        Returns:
            list: Permission class instances.
        """
        if self.action in ['list', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Return filtered queryset based on user role.

        Staff users can see all profiles.
        Regular users can only see their own profile.

        Returns:
            QuerySet: Filtered UserProfile queryset.
        """
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """
        Get or update current user's profile.

        GET: Returns the authenticated user's profile data.
        PATCH: Partially updates the authenticated user's profile.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Profile data or validation errors.
        """
        profile = request.user.profile

        if request.method == 'PATCH':
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class CurrentUserAPIView(APIView):
    """
    API endpoint for current user info.

    GET /accounts/api/v1/me/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return current user's information.

        Args:
            request: The HTTP request object.

        Returns:
            Response: Serialized user data including nested profile.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
