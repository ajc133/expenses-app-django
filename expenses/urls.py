from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("users/", views.users, name="users"),
    path("users/details/<int:id>", views.user_details, name="user_details"),
    path("expenses/", views.expenses, name="expenses"),
    path("expenses/details/<int:id>", views.expense_details, name="expense_details"),
]
