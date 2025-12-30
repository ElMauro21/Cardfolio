from django.urls import path
from .views import register_view,logout_view
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("login/",LoginView.as_view(template_name="accounts/login.html"),name="login"),
    path("logout/",logout_view,name="logout"),
    path("register/",register_view,name="register")
]
