from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    ContactsTemplateView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductTogglePublishView,
    ProductUpdateView, ProductsByCategoryListView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("product/add/", ProductCreateView.as_view(), name="add_product"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="update_product"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="delete_product"),
    path("product/toggle/<int:pk>/", ProductTogglePublishView.as_view(), name="toggle_publish_product"),
    path("category/<int:pk>/", ProductsByCategoryListView.as_view(), name="products_by_category"),
]
