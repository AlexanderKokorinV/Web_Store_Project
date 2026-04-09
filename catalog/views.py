from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse


def home(request):
    return render(request, "catalog/home.html")


def contacts(request):
    if request.method == "POST":
        # Получаем данные из полей
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Добавляем сообщение об успехе
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

    return render(request, "catalog/contacts.html")
