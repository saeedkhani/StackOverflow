from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistreationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        )
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your Password"}
        ),
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your Password"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]

        user = User.objects.filter(email=email).exists()

        if user:
            raise ValidationError("This email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]

        user = User.objects.filter(username=username).exists()

        if user:
            raise ValidationError("This username already exists")
        
        return username

    def clean(self):
        clean_data = super().clean()

        password = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password must match")


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your Password"}
        ),
    )
