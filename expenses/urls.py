from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("expenses/", views.expenses, name="expenses"),
    path("expenses/details/<int:id>", views.details, name="details"),
    path("testing/", views.testing, name="testing"),
]
