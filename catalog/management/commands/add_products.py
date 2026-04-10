from django.core.management import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = "Очищает БД и заполняет её тестовыми данными"

    def handle(self, *args, **options):
        # Очистка базы данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Подготовка данных для категорий
        categories = [
            {"category_name": "Смартфоны", "category_description": "Современные гаджеты"},
            {"category_name": "Ноутбуки", "category_description": "Для работы и игр"},
        ]

        for cat_item in categories:
            category, created = Category.objects.get_or_create(**cat_item)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Успешно добавлена категория: {category.category_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Категория уже существует: {category.category_name}"))

        # Получение объектов категорий из БД, чтобы привязать их к продуктам
        cat_smart = Category.objects.get(category_name="Смартфоны")
        cat_laptop = Category.objects.get(category_name="Ноутбуки")

        # Создание продуктов
        products_data = [
            {
                "product_name": "iPhone 16",
                "category_name": cat_smart,
                "price": 99000,
                "product_description": "С мощным процессором"
            },
            {
                "product_name": "Samsung Galaxy S23",
                "category_name": cat_smart,
                "price": 85000,
                "product_description": "Лучший экран"
            },
            {
                "product_name": "MacBook Air M2",
                "category_name": cat_laptop,
                "price": 120000,
                "product_description": "Тонкий и мощный"
            },
        ]

        for prod_item in products_data:
            product, created = Product.objects.get_or_create(**prod_item)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Успешно добавлен продукт: {product.product_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Продукт уже существует: {product.product_name}"))


        self.stdout.write(self.style.SUCCESS("База данных успешно очищена и заполнена тестовыми данными"))