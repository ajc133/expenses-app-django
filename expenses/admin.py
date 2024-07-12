from django.contrib import admin
from .models import Expense, Payment


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "payer",
        "cost",
        "created_at",
        "updated_at",
        "submitter",
    )


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount")


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Payment, PaymentAdmin)
