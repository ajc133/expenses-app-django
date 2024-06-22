from django.contrib import admin
from .models import Expense, User, Payment


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("item", "description", "cost", "created_at", "updated_at")


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount")


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Payment, PaymentAdmin)
