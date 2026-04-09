from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpRequest


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу каталога."""
    return render(request, "catalog/home.html")


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
