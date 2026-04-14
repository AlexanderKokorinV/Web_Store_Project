from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import ProductForm
from .models import Contact, Product


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу каталога с навигацией."""
    # Все товары, отсортированные по дате создания
    product_list = Product.objects.all().order_by("-created_at")

    # Настройка пагинации (по 3 товара на страницу)
    paginator = Paginator(product_list, 3)

    # Получение номера текущей страницы из URL
    page_number = request.GET.get("page")

    # Получение объекта страницы
    page_obj = paginator.get_page(page_number)

    # Формирование контекста
    context = {
        "page_obj": page_obj,
    }

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


def add_product(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает добавление нового товара.
    Обрабатывает ввод данных и сохраняет новый товар в базу данных.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("catalog:home")  # Перевод на главную страницу после сохранения
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})
