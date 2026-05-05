from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="Моодератор продуктов")
        content_type = ContentType.objects.get_for_model(Product)

        can_unpublish_product = Permission.objects.get(codename="can_unpublish_product", content_type=content_type)
        can_delete_product = Permission.objects.get(codename="can_delete_product", content_type=content_type)

        group.permissions.add(can_unpublish_product, can_delete_product)
        self.stdout.write(self.style.SUCCESS("Группа настроена"))