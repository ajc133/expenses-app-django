from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_expense(cls, item, cost, user_name) -> bool:
        try:
            user = User.objects.filter(name=user_name).get()
        except User.DoesNotExist:
            print(f"User '{user_name}' does not exist")
            return False
        cls(user=user, item=item, cost=cost).save()
        return True

    def __str__(self):
        return f"{self.item}"


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
