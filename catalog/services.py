from catalog.models import Product, Category
from django.core.cache import cache

class ProductService:

    @staticmethod
    def get_all_products():
        """Низкоуровневое кеширование списка всех продуктов"""

        key = "all_products_list"
        products = cache.get(key)

        if products is None:
            products = Product.objects.all()
            cache.set(key, products, 60 * 15)

        return products

    @staticmethod
    def get_products_by_category(category_id):
        """Возвращает список всех продуктов в указанной категории"""
        products = Product.objects.filter(category_name_id=category_id)
        if not products.exists():
            return []

        return products

    @staticmethod
    def get_all_categories():
        """Низкоуровневое кеширование списка всех категорий"""

        key = "all_categories_list"
        categories = cache.get(key)

        if categories is None:
            categories = Category.objects.all()
            cache.set(key, categories, 60 * 60)

        return categories