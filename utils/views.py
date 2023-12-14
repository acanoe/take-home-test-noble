from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.models import UserTypeChoices


# Company owner permissions
class IsOwnerUser(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        is_staff = request.user.is_staff
        is_owner_user = request.user.user_type == UserTypeChoices.OWNER

        return is_authenticated and is_staff and is_owner_user


class IsCompanyOwner(IsOwnerUser):
    def has_permission(self, request, view):
        is_owner_user = super().has_permission(request, view)
        has_company = request.user.company is not None

        return is_owner_user and has_company


# Views
class AuthenticatedAPI(APIView):
    permission_classes = (IsAuthenticated,)


class OwnerUserAPI(APIView):
    permission_classes = (IsOwnerUser,)


class CompanyOwnerAPI(APIView):
    permission_classes = (IsCompanyOwner,)
