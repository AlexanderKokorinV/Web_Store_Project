from django.test import TestCase
from django.urls import reverse

class CatalogViewTests(TestCase):

    def test_home_page_status_code(self):
        """Проверка доступности главной страницы"""
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(response.status_code, 200)

    def test_contacts_page_status_code(self):
        """Проверка доступности страницы контактов"""
        response = self.client.get(reverse("catalog:contacts"))
        self.assertEqual(response.status_code, 200)

    def test_feedback_form_post(self):
        """Проверка отправки формы обратной связи"""
        data = {
            "name": "Test User",
            "phone": "123456789",
            "message": "Hello test message"
        }
        response = self.client.post(reverse("catalog:contacts"), data=data)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе есть сообщение об успехе
        self.assertContains(response, "сообщение")
