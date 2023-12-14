from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import exceptions


class EmailAsUsernameAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                "No active account found with the given credentials."
            )

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect password.")

        return user
