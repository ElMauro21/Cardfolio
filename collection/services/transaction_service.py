from django.db import transaction
from collection.models import UserCard, CardTransaction

def apply_card_transaction(
        *,
        user,
        card,
        transaction_type,
        quantity,
        price_per_unit=None,
):
    """
    Applies a card transaction (BUY or SELL) and updates the user's collection
    in a safe, atomic way.

    This function is the **single source of truth** for modifying a user's
    card holdings. Every change to a user's collection must go through this
    function to ensure that:

    - The user's current holdings (UserCard) remain consistent.
    - A permanent transaction record (CardTransaction) is always created.
    - Invalid operations (e.g. selling more cards than owned) are prevented.
    - Partial updates never occur, thanks to database transactions.

    Conceptually:
    - CardTransaction represents the **historical event** (what happened).
    - UserCard represents the **current snapshot** (what the user owns now).

    Both are updated together inside a single database transaction.

    Parameters
    ----------
    user : AbstractUser
        The user performing the transaction.

    card : Card
        The specific card printing being bought or sold.

    transaction_type : str
        The type of transaction. Must be one of:
        - CardTransaction.BUY
        - CardTransaction.SELL

    quantity : int
        The number of cards involved in the transaction.
        Must be a positive integer.

    price_per_unit : Decimal | None, optional
        The price paid or received per card for this transaction.
        This value is stored on the CardTransaction as historical data.
        It may be None for non-financial adjustments.

    Returns
    -------
    UserCard
        The updated UserCard instance representing the user's current
        holdings after the transaction is applied.

    Raises
    ------
    ValueError
        - If quantity is less than or equal to zero.
        - If attempting to sell more cards than the user owns.
        - If an invalid transaction_type is provided.

    Atomicity
    ----------
    This function runs inside a database transaction (`transaction.atomic()`).

    This guarantees that:
    - Either BOTH the UserCard update and CardTransaction creation succeed.
    - Or NEITHER change is persisted if an error occurs.

    This prevents data corruption and ensures financial consistency.

    Examples
    --------
    Buy 2 copies of a card:

    >>> apply_card_transaction(
    ...     user=user,
    ...     card=card,
    ...     transaction_type=CardTransaction.BUY,
    ...     quantity=2,
    ...     price_per_unit=15.00
    ... )

    Sell 1 copy of a card:

    >>> apply_card_transaction(
    ...     user=user,
    ...     card=card,
    ...     transaction_type=CardTransaction.SELL,
    ...     quantity=1,
    ...     price_per_unit=50.00
    ... )
    """
    if quantity <=0:
        raise ValueError("Quantity must be positive")
    
    with transaction.atomic():
        user_card, _ = UserCard.objects.get_or_create(
            user=user,
            card=card,
            defaults={"quantity":0}
        )

        if transaction_type == CardTransaction.BUY:
            user_card.quantity += quantity
            user_card.save()

        elif transaction_type == CardTransaction.SELL:
            if user_card.quantity < quantity:
                raise ValueError("Not enough cards to sell")
            
            user_card.quantity -= quantity

            if user_card.quantity == 0:
                user_card.delete()
                user_card = None
            else:
                user_card.save()
            
        else: 
            raise ValueError("Invalid transaction type")

        CardTransaction.objects.create(
            user=user,
            card=card,
            transaction_type=transaction_type,
            quantity=quantity,
            price_per_unit=price_per_unit,
        )

        return user_card