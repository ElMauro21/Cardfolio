from collection.models import UserCard
from cards.models import Card
from django.contrib.auth import get_user_model
from django.db import transaction
from typing import TYPE_CHECKING
from django.conf import settings

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser

User = get_user_model()

def add_card_to_collection(
        *,
        user: "AbstractUser",
        card: Card,
        quantity: int =1,
        purchase_price: float | None = None,
) -> UserCard:
    """
    Adds a card to a user's collection.

    If the user already owns the card, the quantity is increased.
    Otherwise, a new collection entry is created.

    This operation is safe against duplicate records and respects
    the unique (user, card) constraint.
    """

    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    
    with transaction.atomic():
        user_card,created = UserCard.objects.get_or_create(
            user = user,
            card = card,
            defaults = {
                "quantity": quantity,
                "purchase_price": purchase_price,
            },
        )

        if not created: 
            user_card.quantity += quantity 

            if purchase_price is not None:
                user_card.purchase_price = purchase_price

            user_card.save()
    return user_card