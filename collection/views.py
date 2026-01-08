from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from collection.forms import AddCardForm
from collection.services.transaction_service import apply_card_transaction
from collection.services.portfolio_service import get_current_portfolio_value
from cards.services.card_importer import import_exact_mtg_card
from collection.models import UserCard
from django.core.paginator import Paginator
from django.db.models import F, Sum, DecimalField, ExpressionWrapper
from collection.models import CardTransaction
from cards.models import Card

@login_required
def my_collection_view(request):
    form = AddCardForm()

    query = request.GET.get("q","").strip()

    collection_qs = (
        request.user.collection
        .select_related("card").annotate(
            subtotal = ExpressionWrapper(
                F("quantity") * F("card__price_usd"),
                output_field=DecimalField(max_digits=12,decimal_places=2)
            )
        )
    )

    if query:
        collection_qs = collection_qs.filter(
            card__name__icontains=query
        )
        
    collection_qs = collection_qs.order_by("card__name")

    paginator = Paginator(collection_qs,10)
    page_number = request.GET.get("page")
    collection_page = paginator.get_page(page_number)
    
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

    total_value = get_current_portfolio_value(request.user)

    return render(request, "collection/my_collection.html", {
        "form": form,
        "collection": collection_page,
        "most_expensive_card": most_expensive_card,
        "query": query,
        "total_value": total_value,
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
            is_foil=data["is_foil"]
        )

        apply_card_transaction(
            user=request.user,
            card=card,
            transaction_type=CardTransaction.BUY,
            quantity=data["quantity"],
            price_per_unit=data.get("purchase_price")
        )

        return redirect("my_collection")
    
@login_required
def remove_card_view(request, usercard_id):
    UserCard.objects.filter(
        id = usercard_id,
        user = request.user
    ).delete()

    return redirect("my_collection")

@login_required
def sell_card_view(request, usercard_id):
    if request.method != "POST":
        return redirect("my_collection")
    
    quantity = int(request.POST["quantity"])
    price = request.POST["price_per_unit"]

    card = Card.objects.get(id=usercard_id)

    apply_card_transaction(
        user=request.user,
        card=card,
        transaction_type=CardTransaction.SELL,
        quantity=quantity,
        price_per_unit=price,
    )

    return redirect("my_collection")




 