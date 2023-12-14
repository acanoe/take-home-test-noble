from django import forms
from django.contrib import admin

from company.models import Company

from .models import User, UserTypeChoices


class SuperuserUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "company",
            "user_type",
            "is_staff",
            "is_superuser",
            "is_active",
            "groups",
            "user_permissions",
            "password",
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "company", "password")

    def clean(self):
        # Check that the company is valid
        company = self.cleaned_data.get("company")
        if not company:
            raise forms.ValidationError("You must select a company for this user.")

        return self.cleaned_data


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = SuperuserUserForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(company=request.user.company)

    def get_list_display(self, request):
        fields = (
            "email",
            "company",
            "user_type",
            "is_superuser",
            "is_active",
        )

        if not request.user.is_superuser:
            return fields[:2]

        return fields

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super().get_form(request, obj, **kwargs)
        return UserForm

    def render_change_form(
        self,
        request,
        context,
        add=False,
        change=False,
        form_url="",
        obj=None,
    ):
        if not request.user.is_superuser:
            fields = context["adminform"].form.fields
            fields["company"].queryset = Company.objects.filter(created_by=request.user)
        return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        # while the user is being created, fill username and user_type fields with
        # default values if needed
        if not change:
            obj.username = form.cleaned_data.get(
                "username",
                form.cleaned_data["email"].replace("@", "_").replace(".", "_"),
            )
            obj.user_type = form.cleaned_data.get("user_type", UserTypeChoices.EMPLOYEE)

        if "password" in form.changed_data:
            # if the user has not been created yet, save the user first
            if not change:
                super().save_model(request, obj, form, change)

            # save the provided password in hashed format
            obj.set_password(form.cleaned_data.get("password", "supersecret"))

        super().save_model(request, obj, form, change)
