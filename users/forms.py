from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

