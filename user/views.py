from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.views import CompanyOwnerAPI

from .models import User, UserTypeChoices
from .serializers import EmployeeSerializer, OwnerSerializer


class OwnerView(APIView):
    serializer_class = OwnerSerializer

    @extend_schema(
        description="Requirement 2: Endpoint to create a owner account.\n\nThis will create a new user with user_type = UserTypeChoices.OWNER with is_staff = True.",
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


class EmployeeView(CompanyOwnerAPI):
    serializer_class = EmployeeSerializer

    @extend_schema(
        description="Requirement 5: Endpoint to show all employee accounts.\n\nThis will list all users with user_type = UserTypeChoices.EMPLOYEE with company set to the logged in user's company.\n\nNote: Only users with user_type = UserTypeChoices.OWNER can list all employee accounts.",
    )
    def get(self, request):
        users = User.objects.filter(
            user_type=UserTypeChoices.EMPLOYEE,
            company=request.user.company,
        )
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Requirement 5: Endpoint to create a employee account.\n\nThis will create a new user with user_type = UserTypeChoices.EMPLOYEE with company set to the logged in user's company.\n\nNote: Only users with user_type = UserTypeChoices.OWNER can create a employee account.",
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
