from django.shortcuts import render
from cards.models import Card

# Create your views here.

def landing_page_view(request):

    cards = Card.objects.order_by("-created_at")[:5]

    return render(request,"core/landing_page.html",{
        "cards": cards
    })