from django.db import models

class Product(models.Model):
    """Модель для хранения информации о продуктах"""
    product_name = models.CharField(max_length=150, verbose_name="Наименование продукта", help_text="Введите наименование продукта")
    product_description = models.TextField(verbose_name="Описание продукта", help_text="Введите описание продукта", blank=True, null=True)
    image = models.ImageField(upload_to="catalog/image", blank=True, null=True, verbose_name="Изображение", help_text="Загрузите изображение")
    category_name = models.ForeignKey(on_delete=models.CASCADE, verbose_name="Категория", related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category_name", "price"]

    def __str__(self):
        return self.product_name



class Category(models.Model):
    """Модель для хранения информации о категориях"""
    category_name = models.CharField(max_length=150, verbose_name="Категория", help_text="Введите название категории")
    category_description = models.TextField(verbose_name="Описание категории", help_text="Введите описание категории", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.category_name