from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="expenses"), name="main"),
    path("users/", views.users, name="users"),
    path("users/details/<int:expense_id>", views.user_details, name="user_details"),
    path("expenses/", views.expenses, name="expenses"),
    path(
        "expenses/<int:expense_id>/details",
        views.expense_details,
        name="expense_details",
    ),
    path("expenses/<int:expense_id>/edit", views.expense_edit, name="expense_edit"),
]
