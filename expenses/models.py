from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

receipts = FileSystemStorage(location="./receipts")


class Expense(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    cost = models.FloatField()
    submitter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expense_submitter", null=False
    )
    receipt_photo = models.ImageField(upload_to="receipts", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     do_something()
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
    #     do_something_else()
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
