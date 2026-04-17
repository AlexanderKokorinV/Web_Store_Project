from typing import Any

from django.db import models


class BlogPost(models.Model):
    """Модель для хранения блоговых записей"""

    title: Any = models.CharField(max_length=150, verbose_name="Заголовок", help_text="Введите заголовок поста")
    content: Any = models.TextField(verbose_name="Содержимое", help_text="Введите содержимое поста")
    preview: Any = models.ImageField(
        upload_to="blog_previews", verbose_name="Превью (изображение)", null=True, blank=True
    )
    created_at: Any = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published: Any = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_count: Any = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self) -> str:
        """Возвращает строковое представление модели (заголовок)"""
        return str(self.title)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-created_at"]
