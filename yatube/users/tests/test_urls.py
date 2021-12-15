from http import HTTPStatus

from django.test import Client, TestCase

from posts.models import User
from posts.tests import const


class UsersURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(
            username=const.USERNAME_REG
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_templates_urls_users(self):
        """Проверяем доступность страниц и соответствие
        шаблонов URL приложения users.
        """
        template_urls = {
            '/auth/signup/': [
                const.SIGNUP_TEMPLATE,
                self.guest_client,
                HTTPStatus.OK.value,
            ],
            '/auth/login/': [
                const.LOGIN_TEMPLATE,
                self.guest_client,
                HTTPStatus.OK.value,
            ],
            '/auth/logout/': [
                const.LOGOUT_TEMPLATE,
                self.guest_client,
                HTTPStatus.OK.value,
            ],
            '/auth/password_change/done/': [
                const.PASS_CHANGE_DONE_TEMPLATE,
                self.guest_client,
                HTTPStatus.OK.value,
            ],
            '/auth/password_change/': [
                const.PASS_CHANGE_TEMPLATE,
                self.authorized_client,
                HTTPStatus.OK.value,
            ],
        }
        for adress, [template, authoriz, st_code] in template_urls.items():
            with self.subTest(adress=adress):
                response = authoriz.get(adress)
                self.assertEqual(
                    response.status_code,
                    st_code,
                )
                self.assertTemplateUsed(response, template)
