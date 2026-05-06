from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .forms import ProductForm
from .models import Contact, Product, Category
from .services import ProductService


@method_decorator(cache_page(60 * 15), name="dispatch") # Кеширование страницы списка продуктов на 15 мин.
class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"  # Путь к шаблону
    context_object_name = "product_list"
    paginate_by = 3
    ordering = ["-created_at"]

    def get_queryset(self):
        return ProductService.get_all_products()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ProductService.get_all_categories() # Получаем все категории для фильтров
        return context

@method_decorator(cache_page(60 * 15), name="dispatch") # Кеширование детальной страницы продукта на 15 мин.
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Купить {self.object.product_name}"
        return context

@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductsByCategoryListView(ListView):
    model = Product
    template_name = "catalog/products_by_category.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category_pk = self.kwargs.get("pk")
        return ProductService.get_products_by_category(self.category_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(pk=self.category_pk)
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user  # Назначаем владельца
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        # Логика: если НЕ владелец И НЕ модератор И НЕ суперюзер -> Вход воспрещен
        if self.object.owner != user and not user.has_perm("catalog.can_unpublish_product") and not user.is_superuser:
            raise PermissionDenied

        return self.object

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Скрываем поле только для тех, кто не модератор
        if not self.request.user.has_perm("catalog.can_unpublish_product"):
            if "is_published" in form.fields:
                del form.fields["is_published"]
        return form


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user

        if self.object.owner != user and not user.has_perm("catalog.delete_product") and not user.is_superuser:
            raise PermissionDenied

        return self.object


class ProductTogglePublishView(PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.is_published:
            product.is_published = False
            messages.warning(request, f"Продукт '{product.product_name}' снят с публикации.")
        else:
            product.is_published = True
            messages.success(request, f"Продукт '{product.product_name}' успешно опубликован!")

        product.save()

        return redirect(reverse("catalog:product_detail", args=[product.pk]))


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"
    success_url = reverse_lazy("catalog:contacts")

    def get_context_data(self, **kwargs):
        """Передает данные о контактах из базы в шаблон"""
        context = super().get_context_data(**kwargs)
        context["contact"] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        """ "Обработка POST-запроса (данных из формы)"""
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(f"Сообщение от {name}, {email}: {message}")

        return redirect(self.success_url)


# Ниже в комментариях код с использованием FBV:

# def home(request: HttpRequest) -> HttpResponse:
#     """Отображает главную страницу каталога с навигацией."""
#     # Все товары, отсортированные по дате создания
#     product_list = Product.objects.all().order_by("-created_at")
#
#     # Настройка пагинации (по 3 товара на страницу)
#     paginator = Paginator(product_list, 3)
#
#     # Получение номера текущей страницы из URL
#     page_number = request.GET.get("page")
#
#     # Получение объекта страницы
#     page_obj = paginator.get_page(page_number)
#
#     # Формирование контекста
#     context = {
#         "page_obj": page_obj,
#     }
#
#     return render(request, "catalog/home.html", context)


# def contacts(request: HttpRequest) -> HttpResponse:
#     """
#     Обрабатывает страницу контактов.
#     При GET-запросе возвращает страницу с формой обратной связи.
#     При POST-запросе принимает данные формы и возвращает сообщение об успехе.
#     """
#
#     # Получаем данные из базы
#     contact_data = Contact.objects.first()
#
#     if request.method == "POST":
#         # Получаем данные из полей
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")
#
#         # Добавляем сообщение
#         print(f"Сообщение от {name} ({email}): {message}")
#
#     return render(request, "catalog/contacts.html", {"contact": contact_data})


# def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
#     """Отображает детальную информацию о конкретном товаре."""
#     product = Product.objects.get(pk=pk)
#     context = {"object": product, "title": f"Купить {product.product_name}"}
#     return render(request, "catalog/product_detail.html", context)


# def add_product(request: HttpRequest) -> HttpResponse:
#     """
#     Обрабатывает добавление нового товара.
#     Обрабатывает ввод данных и сохраняет новый товар в базу данных.
#     """
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("catalog:home")  # Перевод на главную страницу после сохранения
#     else:
#         form = ProductForm()
#
#     return render(request, "catalog/product_form.html", {"form": form})
