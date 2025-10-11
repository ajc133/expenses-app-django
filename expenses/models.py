from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return "receipts/user_{0}/{1}".format(instance.submitter.id, filename)


class Expense(models.Model):
    payer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expenses_paid"
    )
    item = models.CharField(max_length=255)
    cost = models.FloatField()
    submitter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expenses_submitted", null=False
    )
    group = models.ForeignKey(
        "auth.Group", on_delete=models.CASCADE, related_name="expenses", null=False
    )
    receipt_photo = models.ImageField(upload_to="receipts", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item} bought by {self.payer.first_name}"
