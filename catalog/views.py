from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Contact, Product


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу каталога."""
    latest_products = Product.objects.order_by("-created_at")[:5]

    print("\nПоследние 5 продуктов:")
    for product in latest_products:
        print(f"ID: {product.id} | Название: {product.product_name} | Дата: {product.created_at}")
    print("-" * 25)

    context = {"object_list": latest_products}

    return render(request, "catalog/home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает страницу контактов.
    При GET-запросе возвращает страницу с формой обратной связи.
    При POST-запросе принимает данные формы и возвращает сообщение об успехе.
    """

    # Получаем данные из базы
    contact_data = Contact.objects.first()

    if request.method == "POST":
        # Получаем данные из полей
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Добавляем сообщение
        print(f"Сообщение от {name} ({email}): {message}")

    return render(request, "catalog/contacts.html", {"contact": contact_data})


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Отображает детальную информацию о конкретном товаре."""
    product = Product.objects.get(pk=pk)
    context = {"object": product, "title": f"Купить {product.product_name}"}
    return render(request, "catalog/product_detail.html", context)



