from django import forms
from .models import Account
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "phone_number", "password"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter Email Address"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Phone Number"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Enter Password"}
            ),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error("password", e)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data
