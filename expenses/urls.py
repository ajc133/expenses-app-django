from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
