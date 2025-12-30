from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from .forms import RegisterForm

def register_view(request):
    """
    Handles user registration.

    - Redirects authenticated users away from the registration page.
    - Displays the registration form on GET requests.
    - Validates and creates a new user on POST requests using RegisterForm.
    - Automatically logs the user in after successful registration.
    """
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data["username"],
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"]
            )
            login(request, user)
            return redirect("home")
    else: 
        form = RegisterForm()
    
    return render(request, "accounts/register.html",{"form": form})

def logout_view(request):
    """
    Logs the current user out and redirects to the home page.

    Clears the session and removes authentication data
    without modifying the user record.
    """
    logout(request)
    return redirect("home")