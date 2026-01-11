from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_collection_view, name="my_collection"),
    path("add/", views.add_card_view, name="add_card"),
    path("sell/<int:usercard_id>",views.sell_card_view,name="sell_card"),
]
