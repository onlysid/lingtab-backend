from django.db import models

# Model for transactions made by users
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Handles amounts up to 999,999,999.99
    description = models.TextField(blank=True, null=True)  # Optional field to describe the transaction
    date = models.DateTimeField(auto_now_add=True)  # Automatically sets the timestamp when the transaction is created
    repayment = models.BooleanField(default=False)  # Tracks which way the transaction is going

    def __str__(self):
        status = "Paid" if self.is_paid else "Spent"
        return f"{self.user.username} {status} {self.amount}"
