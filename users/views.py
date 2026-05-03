import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()  # Сохраняем пользователя
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        messages.success(
            self.request,
            f"Регистрация почти завершена! На адрес {user.email} отправлена ссылка для подтверждения вашей почты.",
        )
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{user.token}/"

        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте, {user.email}! Спасибо за регистрацию на нашем сайте! Для подтверждения почты перейдите по ссылке: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None
    user.save()
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")
    success_message = "Профиль успешно обновлен!"

    def get_object(self, queryset=None):
        return self.request.user
