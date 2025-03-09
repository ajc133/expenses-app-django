from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

photos = FileSystemStorage(location="./photos")


class Expense(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    cost = models.FloatField()
    submitter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expense_submitter", null=False
    )
    receipt_photo = models.ImageField(upload_to="photos", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item} bought by {self.payer.first_name}"


class Payment(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments_sent"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments_received"
    )
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
