from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blog.models import BlogPost


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создаем группу
        group, _ = Group.objects.get_or_create(name="Контент-менеджер")

        # Получаем тип контента
        content_type = ContentType.objects.get_for_model(BlogPost)

        # Получаем стандартные права
        permissions = Permission.objects.filter(content_type=content_type)

        # Назначаем права группе
        group.permissions.add(*permissions)

        # Выводим сообщение
        self.stdout.write(self.style.SUCCESS("Группа настроена"))