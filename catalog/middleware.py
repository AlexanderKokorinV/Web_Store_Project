from django.shortcuts import redirect
from django.urls import reverse


class CatalogAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if any(
            [
                request.path.startswith("/admin/"),
                request.path.startswith("/static/"),
                request.path.startswith("/media/"),
            ]
        ):
            return self.get_response(request)

        allowed_paths = [
            reverse("catalog:home"),
            reverse("users:login"),
            reverse("users:register"),
            reverse("users:password_reset"),
            reverse("users:password_reset_done"),
            reverse("users:password_reset_complete"),
        ]

        if not request.user.is_authenticated:
            is_allowed_path = request.path in allowed_paths
            is_confirm_email = request.path.startswith("/users/email-confirm/")
            is_confirm_password = request.path.startswith("/users/password-reset-confirm/")
            is_verification_path = request.path.startswith("/users/email-confirm/")

            if not (is_allowed_path or is_verification_path or is_confirm_email or is_confirm_password):
                return redirect(reverse("users:login"))

        return self.get_response(request)
