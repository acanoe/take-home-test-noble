from django.db import IntegrityError
from rest_framework import exceptions, serializers, status

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "industry"]

    def validate(self, data):
        if self.context["request"].user.company:
            raise exceptions.APIException(
                "Cannot create company. User already has a company.",
                status.HTTP_400_BAD_REQUEST,
            )
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user

        try:
            company = Company.objects.create(**validated_data)

            user.company = company
            user.save()

            return company
        except IntegrityError as e:
            raise exceptions.APIException(
                f"Cannot create company: {e}",
                status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise exceptions.APIException(
                f"Unexpected error: {e}",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
