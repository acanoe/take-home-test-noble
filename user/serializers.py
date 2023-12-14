from rest_framework import serializers

from .models import User, UserTypeChoices


class BaseUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)


class OwnerSerializer(BaseUserSerializer):
    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "Company owner with this email already exists.",
            )
        return data

    def create(self, validated_data):
        validated_data.update(
            {
                "username": validated_data["email"].split("@")[0],
                "user_type": UserTypeChoices.OWNER,
                "is_staff": True,
            }
        )
        return User.objects.create_user(**validated_data)


class EmployeeSerializer(BaseUserSerializer):
    company = serializers.CharField(max_length=128, read_only=True)

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "Employee with this email already exists.",
            )
        return data

    def create(self, validated_data):
        validated_data.update(
            {
                "username": validated_data["email"].split("@")[0],
                "user_type": UserTypeChoices.EMPLOYEE,
                "company": self.context["request"].user.company,
            }
        )
        return User.objects.create_user(**validated_data)
