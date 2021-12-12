from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

import posts.tests.const as const
from posts.models import Group, Post, User


class PostsURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME_AUTH)
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.SLUG,
            description=const.DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=const.TEXT,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=const.USERNAME_REG)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.post.author)

    def test_templates(self):
        """Проверяем доступность страниц и соответствие
        шаблонов URL приложения posts.
        """
        cache.clear()
        template_urls = {
            '/group/test_slug/': [
                const.GROUP_POSTS_TEMPLATE,
                'guest',
                HTTPStatus.OK.value,
            ],
            '/profile/Tester/': [
                const.PROFILE_TEMPLATE,
                'guest',
                HTTPStatus.OK.value,
            ],
            '/posts/1/': [
                const.POST_DETAIL_TEMPLATE,
                'guest',
                HTTPStatus.OK.value,
            ],
            '/': [
                const.INDEX_TEMPLATE,
                'guest',
                HTTPStatus.OK.value,
            ],
            '/create/': [
                const.POST_CREATE_TEMPLATE,
                'reg',
                HTTPStatus.FOUND.value,
            ],
            '/posts/1/edit/': [
                const.POST_CREATE_TEMPLATE,
                'author',
                HTTPStatus.FOUND.value,
            ],
        }

        for adress, [template, authoriz, st_code] in template_urls.items():
            with self.subTest(adress=adress):
                cache.clear()
                response = self.guest_client.get(adress)
                self.assertEqual(
                    response.status_code,
                    st_code,
                )
                if authoriz == 'guest':
                    self.assertTemplateUsed(response, template)
                    cache.clear()
                    response = self.authorized_client.get(adress)
                    self.assertEqual(
                        response.status_code,
                        st_code,
                    )
                    self.assertTemplateUsed(response, template)
                    cache.clear()
                    response = self.author_client.get(adress)
                    self.assertEqual(
                        response.status_code,
                        st_code,
                    )
                    self.assertTemplateUsed(response, template)
                if authoriz == 'reg':
                    cache.clear()
                    response = self.authorized_client.get(adress)
                    self.assertEqual(
                        response.status_code,
                        HTTPStatus.OK.value,
                    )
                    self.assertTemplateUsed(response, template)
                if authoriz == 'author':
                    cache.clear()
                    response = self.author_client.get(adress)
                    self.assertEqual(
                        response.status_code,
                        HTTPStatus.OK.value,
                    )
                    self.assertTemplateUsed(response, template)

    def test_unexisting_page(self):
        """Проверка ответа на запрос несуществующей страницы"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)
