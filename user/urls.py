from django.urls import path

from .views import EmployeeView, OwnerView

urlpatterns = [
    path("employees/", EmployeeView.as_view()),
    path("owners/", OwnerView.as_view()),
]
