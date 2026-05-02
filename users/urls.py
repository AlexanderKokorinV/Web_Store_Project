from users.apps import UsersConfig
from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import CustomLoginView

from users.views import UserRegisterView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
]