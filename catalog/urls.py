from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts

APP_NAME = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
]
