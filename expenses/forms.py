from django import forms


class ExpenseForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
