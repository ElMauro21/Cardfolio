from django.urls import path
from .views import landing_page_view,learn_more_view

urlpatterns = [
    path("",landing_page_view,name="home"),
    path("learn-more/",learn_more_view,name="learn-more")
]
