from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("users/", views.users, name="users"),
    path("users/details/<int:id>", views.user_details, name="user_details"),
    path("expenses/", views.expenses, name="expenses"),
    path("expenses/<int:id>/details", views.expense_details, name="expense_details"),
    path("expenses/<int:id>/edit", views.expense_edit, name="expense_edit"),
]
