from catalog.models import Product


class ProductService:

    @staticmethod
    def get_products_by_category(category_id):
        """Возвращает список всех продуктов в указанной категории"""
        products = Product.objects.filter(category_id=category_id)
        if not products.exists():
            return []
        return products