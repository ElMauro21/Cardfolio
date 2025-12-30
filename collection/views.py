from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from collection.forms import AddCardForm
from collection.services.collection_service import add_card_to_collection
from cards.services.card_importer import import_exact_mtg_card
from .models import UserCard
from collection.models import UserCard

@login_required
def my_collection_view(request):
    form = AddCardForm()
    collection = (
        request.user.collection.select_related("card").order_by("-added_at")
    )
    
    most_expensive_card = (
        UserCard.objects
        .filter(
            user = request.user,
            card__price_usd__isnull = False
        )
        .select_related("card")
        .order_by("-card__price_usd")
        .first()
    )

    return render(request, "collection/my_collection.html", {
        "form": form,
        "collection": collection,
        "most_expensive_card": most_expensive_card
    })

@login_required
def add_card_view(request):
    """
    Allows an authenticated user to add a card to their collection.
    """
    if request.method != "POST":
        return redirect("my_collection")
    
    form = AddCardForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data

        card = import_exact_mtg_card(
            set_code=data["set_code"],
            collector_number=data["collector_number"],
        )

        add_card_to_collection(
            user=request.user,
            card=card,
            quantity=data["quantity"],
            purchase_price=data.get("purchase_price"),
        )

        return redirect("my_collection")
    
@login_required
def remove_card_view(request, usercard_id):
    UserCard.objects.filter(
        id = usercard_id,
        user = request.user
    ).delete()

    return redirect("my_collection")





 