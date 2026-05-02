from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import UserRegisterForm
from users.models import User

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save() # Сохраняем пользователя
        user.is_active = False

