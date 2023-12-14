from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from utils.views import OwnerUserAPI

from .serializers import CompanySerializer


class CompanyView(OwnerUserAPI):
    serializer_class = CompanySerializer

    @extend_schema(
        description="Requirement 4: Endpoint to create a company.\n\nThis will create a new company with created_by set to the logged in user.\n\nNote: Only users with user_type = UserTypeChoices.OWNER can create a company, and they cannot create another company.",
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
