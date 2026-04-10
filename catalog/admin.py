from django.contrib import admin
from catalog.models import Product, Category, Contact


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "price", "category_name",)
    list_filter = ("category_name",)
    search_fields = ("product_name", "description",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name",)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("country", "inn", "address",)