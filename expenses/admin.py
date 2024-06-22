from django.contrib import admin
from .models import Expense, User


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("item", "description", "cost", "created_at", "updated_at")


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(User, UserAdmin)
