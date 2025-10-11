from django.contrib import admin
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "payer",
        "cost",
        "created_at",
        "updated_at",
        "submitter",
        "group",
    )


admin.site.register(Expense, ExpenseAdmin)
