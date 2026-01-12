from django.urls import path
from .views import register_view,logout_view
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/",LoginView.as_view(template_name="accounts/login.html"),name="login"),
    path("logout/",logout_view,name="logout"),
    path("register/",register_view,name="register"),
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
