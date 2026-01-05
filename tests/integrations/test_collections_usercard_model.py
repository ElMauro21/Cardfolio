import pytest

from collection.models import UserCard
from django.db import IntegrityError


@pytest.mark.integration
def test_usercard_unique_constraint(db, user, card):
    UserCard.objects.create(user=user, card=card, quantity=1)

    with pytest.raises(IntegrityError):
        UserCard.objects.create(user=user, card=card, quantity=1)
