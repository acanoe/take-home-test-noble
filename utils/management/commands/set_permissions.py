from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from company.models import Company
from user.models import User


class Command(BaseCommand):
    help = "Set permissions for groups, and add staff users to groups."

    def add_arguments(self, parser):
        parser.add_argument("user", help="User email", nargs="+", type=str)

    def handle(self, *args, **options):
        GROUP_NAME = "CompanyOwner"
        ALLOWED_MODELS = [User, Company]
        ALLOWED_OPERATIONS = ["add", "view"]

        # Create group
        group, created = Group.objects.get_or_create(name=GROUP_NAME)

        # Add permissions
        for model in ALLOWED_MODELS:
            for operation in ALLOWED_OPERATIONS:
                try:
                    permission = Permission.objects.get(
                        content_type__model=model._meta.model_name,
                        codename=f"{operation}_{model._meta.model_name}",
                    )
                    group.permissions.add(permission)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Permission {operation}_{model._meta.model_name} added to {GROUP_NAME}."
                        )
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Permission {operation}_{model._meta.model_name} does not exist."
                        )
                    )

        # Add all staff users to group if no users are specified
        if not options["user"]:
            staff_users = User.objects.filter(is_staff=True)
            if staff_users.exists():
                group.user_set.add(*staff_users)

            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(staff_users)} staff users added to {GROUP_NAME}."
                )
            )
        else:
            # Add specified users to group
            for user in options["user"]:
                try:
                    user = User.objects.get(email=user)
                    group.user_set.add(user)

                    self.stdout.write(
                        self.style.SUCCESS(f"User {user.email} added to {GROUP_NAME}.")
                    )
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"User {user} does not exist."))
