from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.views import CompanyOwnerAPI

from .models import User, UserTypeChoices
from .serializers import EmployeeSerializer, OwnerSerializer


class OwnerView(APIView):
    serializer_class = OwnerSerializer

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

    def get(self, request):
        users = User.objects.filter(
            user_type=UserTypeChoices.EMPLOYEE,
            company=request.user.company,
        )
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
