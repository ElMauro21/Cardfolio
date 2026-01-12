from django.shortcuts import render
from cards.models import Card

# Create your views here.

def landing_page_view(request):
    """
    Renders the landing page.

    Displays the most recently added cards to provide
    a visual preview of the platform's content.
    """
    cards = Card.objects.order_by("-created_at")[:5]

    return render(request,"core/landing_page.html",{
        "cards": cards
    })

def learn_more_view(request): 
    """
    Renders the learn more page.
    """
    return render(request,"core/learn_more.html")