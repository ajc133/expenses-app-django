from django import forms
from django.contrib.auth.models import User, Group
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["payer", "group", "item", "cost", "receipt_photo"]
        widgets = {
            "receipt_photo": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Show first name on the dropdown if available
        self.fields["payer"].label_from_instance = (
            lambda obj: obj.first_name or obj.username
        )

        # Restrict group choices to only those the current user belongs to
        # FIXME: Only show users that are in current user's groups
        if group is not None:
            groups = Group.objects.filter(pk=group.id)
            self.fields["group"].queryset = groups
            self.fields["payer"].queryset = User.objects.filter(
                groups__in=groups
            ).distinct()
