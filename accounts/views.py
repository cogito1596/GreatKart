from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account, MyAccountManager

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login(request):
    return render(request, "accounts/login.html")


def logout(request):
    return
