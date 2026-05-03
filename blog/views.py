from typing import Optional

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.models import BlogPost


# Create
class BlogPostCreateView(CreateView):
    """Контроллер для создания новой блоговой записи"""

    model = BlogPost
    template_name = "blog/blog_post_form.html"
    fields = ("title", "content", "preview", "is_published")
    success_url = reverse_lazy("blog:blog_post_list")


# Read
class BlogPostListView(ListView):
    """Контроллер для отображения списка опубликованных блоговых записей"""

    model = BlogPost
    template_name = "blog/blog_post_list.html"

    def get_queryset(self) -> QuerySet:
        """Возвращает список только опубликованных записей"""
        return super().get_queryset().filter(is_published=True)  # Показываем только опубликованные записи


# Details (Read)
class BlogPostDetailView(DetailView):
    """Контроллер для детального просмотра статьи со счетчиком просмотров"""

    model = BlogPost
    template_name = "blog/blog_post_detail.html"

    def get_object(self, queryset: Optional[QuerySet] = None) -> BlogPost:
        """Увеличивает счетчик просмотров и отправляет уведомление при достижении порога
        Принимает queryset: базовый набор данных для поиска объекта
        Возвращает BlogPost: объект блоговой записи
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count % 5 == 0:
            full_url = self.request.build_absolute_uri(reverse("blog:blog_post_detail", kwargs={"pk": self.object.pk}))

            send_mail(
                subject=f"У статьи {self.object.views_count} просмотров!",
                message=(
                    f"Вау! Ваша статья '{self.object.title}'\n"
                    f"набрала уже {self.object.views_count} просмотров!\n\n"
                    f"Ссылка на статью: {full_url}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["sanya.core@gmail.com"],
            )

        return self.object  # type: ignore


# Update
class BlogPostUpdateView(UpdateView):
    """Контроллер для редактирования существующей блоговой записи"""

    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_post_form.html"

    def get_success_url(self) -> str:
        """ "Возвращает URL-адрес для перенаправления после успешного редактирования"""
        return reverse("blog:blog_post_detail", kwargs={"pk": self.object.pk})


# Delete
class BlogPostDeleteView(DeleteView):
    """Контроллер для удаления блоговой записи"""

    model = BlogPost
    template_name = "blog/blog_post_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_post_list")
