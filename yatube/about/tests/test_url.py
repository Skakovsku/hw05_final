from django.test import Client, TestCase


class AboutURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_about_url(self):
        """Проверяем доступность страниц и шаблонов приложения about."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/author.html')
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/tech.html')
