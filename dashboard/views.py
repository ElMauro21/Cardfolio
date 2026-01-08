from django.shortcuts import render
from collection.services.portfolio_service import get_current_portfolio_value
from decimal import Decimal

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render 
from dashboard.services.dashboard_service import (
    get_total_invested, 
    get_total_earned, 
    get_unrealized_pl,
    get_roi_percentage,
    get_total_roi_percentage)

@login_required
def dashboard_view(request):
    total_invested = get_total_invested(request.user)
    total_earned = get_total_earned(request.user)
    current_portfolio_value = get_current_portfolio_value(request.user)
    unrealized_profit_loss = get_unrealized_pl(request.user)
    roi = get_roi_percentage(request.user)
    total_roi = get_total_roi_percentage(request.user)

    return render(request, "dashboard/dashboard.html",{
        "total_invested": total_invested,
        "total_earned": total_earned,
        "current_portfolio_value": current_portfolio_value,
        "unrealized_profit_loss": unrealized_profit_loss,
        "roi": roi,
        "total_roi":total_roi
    })