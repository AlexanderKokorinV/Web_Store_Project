from django.shortcuts import redirect
from django.urls import reverse


class CatalogAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем системные папки статики, медиа и админки сразу
        if any(
            [
                request.path.startswith("/admin/"),
                request.path.startswith("/static/"),
                request.path.startswith("/media/"),
            ]
        ):
            return self.get_response(request)

        # Если пользователь уже авторизован - отдаем страницу без проверок
        if request.user.is_authenticated:
            return self.get_response(request)

        # Разрешения для неавторизованных гостей сайта
        allowed_paths = [
            reverse("catalog:home"),
            reverse("catalog:contacts"),
            reverse("users:login"),
            reverse("users:register"),
            reverse("users:password_reset"),
            reverse("users:password_reset_done"),
            reverse("users:password_reset_complete"),
        ]

        is_allowed_path = request.path in allowed_paths
        is_confirm_email = request.path.startswith("/users/email-confirm/")
        is_confirm_password = request.path.startswith("/users/password-reset-confirm/")

        # Если гость пытается открыть закрытую страницу - отправляется на логин
        if not (is_allowed_path or is_confirm_email or is_confirm_password):
            return redirect(reverse("users:login"))

        return self.get_response(request)
