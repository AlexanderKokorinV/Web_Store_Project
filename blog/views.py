from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings

from blog.models import BlogPost


# Create
class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = "blog/blog_post_form.html"
    fields = ("title", "content", "preview", "is_published")
    success_url = reverse_lazy("blog:blog_post_list")

# Read
class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blog_post_list.html"

    def get_queryset(self):

        return super().get_queryset().filter(is_published=True) # Показываем только опубликованные записи

# Details (Read)
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_post_detail.html"

    def get_object(self, queryset=None):

        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count % 5 == 0:
            full_url = self.request.build_absolute_uri(
                reverse("blog:blog_post_detail", kwargs={"pk": self.object.pk})
            )

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

        return self.object

# Update
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_post_form.html"

    def get_success_url(self):
        return reverse("blog:blog_post_detail", kwargs={"pk": self.object.pk})

# Delete
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blog_post_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_post_list")


