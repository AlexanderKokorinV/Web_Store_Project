from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from .models import Product


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу каталога."""
    latest_products = Product.objects.order_by('-created_at')[:2]

    print("\nПоследние 5 продуктов:")
    for product in latest_products:
        print(f"ID: {product.id} | Название: {product.product_name} | Дата: {product.created_at}")
    print("-" * 25)

    context = {
        'object_list': latest_products
    }

    return render(request, "catalog/home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает страницу контактов.
    При GET-запросе возвращает страницу с формой обратной связи.
    При POST-запросе принимает данные формы и возвращает сообщение об успехе.
    """
    if request.method == "POST":
        # Получаем данные из полей
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Добавляем сообщение об успехе
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

    return render(request, "catalog/contacts.html")
