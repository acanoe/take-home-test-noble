from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.models import UserTypeChoices


# Company owner permissions
class IsOwnerUser(IsAuthenticated):
    def has_permission(self, request, view):
        # will not check other conditions if user is not authenticated
        if not super().has_permission(request, view):
            return False

        is_staff = request.user.is_staff
        is_owner_user = request.user.user_type == UserTypeChoices.OWNER

        return is_staff and is_owner_user


class IsCompanyOwner(IsOwnerUser):
    def has_permission(self, request, view):
        # will not check the other condition if user_type is not OWNER
        if not super().has_permission(request, view):
            return False

        return request.user.company is not None


# Views
class AuthenticatedAPI(APIView):
    permission_classes = (IsAuthenticated,)


class OwnerUserAPI(APIView):
    permission_classes = (IsOwnerUser,)


class CompanyOwnerAPI(APIView):
    permission_classes = (IsCompanyOwner,)
