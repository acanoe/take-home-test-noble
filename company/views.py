from rest_framework import status
from rest_framework.response import Response

from utils.views import OwnerUserAPI

from .serializers import CompanySerializer


class CompanyView(OwnerUserAPI):
    serializer_class = CompanySerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
