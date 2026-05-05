from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create_user(email="kokorinalexander@yandex.ru")
        user.set_password("123")
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("Суперпользователь создан"))