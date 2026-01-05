from django.db import models
from cards.models import Card
from django.conf import settings

# Create your models here.

class UserCard(models.Model):
    """
    Represents a card owned by a user as part of their collection.

    This model links a user to a specific card printing and stores
    collection-specific data such as quantity and purchase price.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="collection"
    )

    card = models.ForeignKey(
        Card,
        on_delete = models.CASCADE,
        related_name="owners"
    )

    quantity = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user","card"],
                name="unique_user_card"
            )
        ]

    def __str__(self):
        return f"{self.user} owns {self.quantity} x {self.card}"
    
class CardTransaction(models.Model):
    BUY = "buy"
    SELL = "sell"

    TRANSACTION_TYPES = [
        (BUY,"Buy"),
        (SELL,"Sell"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="card_transactions"
    )

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    quantity = models.PositiveIntegerField()

    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sign = "+" if self.transaction_type == self.BUY else "-"
        return f"{self.user} {sign}{self.quantity} {self.card}"