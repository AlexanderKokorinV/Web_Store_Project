from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import add_product, contacts, home, product_detail

APP_NAME = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:pk>", product_detail, name="product_detail"),
    path("product/add/", add_product, name="add_product"),
]
