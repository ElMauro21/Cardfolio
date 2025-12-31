from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from collection.forms import AddCardForm
from collection.services.collection_service import add_card_to_collection
from cards.services.card_importer import import_exact_mtg_card
from .models import UserCard
from collection.models import UserCard
from django.core.paginator import Paginator

@login_required
def my_collection_view(request):
    form = AddCardForm()

    query = request.GET.get("q","").strip()

    collection_qs = (
        request.user.collection
        .select_related("card")
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

    return render(request, "collection/my_collection.html", {
        "form": form,
        "collection": collection_page,
        "most_expensive_card": most_expensive_card,
        "query": query
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





 