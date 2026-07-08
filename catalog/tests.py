from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CatalogViewTests(TestCase):
    """Тесты для приложения catalog"""

    def setUp(self):
        """Создание тестового пользователя перед каждым тестом"""
        User = get_user_model()

        self.user = User.objects.create(email="test@test.com", is_active=True)
        self.user.set_password("1234!1234")
        self.user.save()

    def test_home_page_status_code(self) -> None:
        """Проверка доступности главной страницы"""
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page_status_code(self) -> None:
        """Проверка доступности страницы контактов для авторизованного пользователя"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("catalog:contacts"))
        self.assertEqual(response.status_code, 200)

    def test_feedback_form_post(self) -> None:
        """Проверка отправки формы обратной связи"""
        self.client.force_login(self.user)
        data = {"name": "Test User", "phone": "123456789", "message": "Hello test message"}
        response = self.client.post(reverse("catalog:contacts"), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе есть сообщение об успехе
        self.assertContains(response, "сообщение")
