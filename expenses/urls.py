from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="submit/")),
    path("expenses/", RedirectView.as_view(url="groups/")),
    path("submit/", views.submit_expense, name="expense_submit"),
    path("groups/", views.groups, name="groups"),
    path("groups/<int:group_id>", views.group_expenses, name="group_expenses"),
    path(
        "expenses/<int:expense_id>/details",
        views.expense_details,
        name="expense_details",
    ),
    path("expenses/<int:expense_id>/edit", views.expense_edit, name="expense_edit"),
    path(
        "expenses/<int:expense_id>/delete", views.expense_delete, name="expense_delete"
    ),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
