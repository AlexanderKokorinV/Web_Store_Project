from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Класс для создания суперпользователя"""

    def handle(self, *args, **options):
        # Создаем суперпользователя
        if not User.objects.filter(email="kokorinalexander@yandex.ru").exists():
            User.objects.create_superuser(email="kokorinalexander@yandex.ru", password="1234!1234")
            self.stdout.write(self.style.SUCCESS("Суперпользователь создан"))
        else:
            self.stdout.write(self.style.WARNING("Пользователь уже существует"))
