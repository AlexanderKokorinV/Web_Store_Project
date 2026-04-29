from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsTemplateView, ProductCreateView, ProductDetailView, ProductListView, \
    ProductUpdateView, ProductDeleteView

APP_NAME = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("product/add/", ProductCreateView.as_view(), name="add_product"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="update_product"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete_product"),
]
