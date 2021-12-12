from django.conf import settings
from django.test import Client, TestCase

import posts.tests.const as const
from posts.models import Group, Post, User


class PaginatorViewsTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=const.USERNAME_AUTH)
        self.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.SLUG,
            description=const.DESCRIPTION,
        )
        for i in range(1, 14):
            self.post = Post.objects.create(
                author=self.user,
                text='Тестовый пост номер ' + str(i),
                group=self.group
            )

    def test_first_page_contains_ten_records(self):
        """Проверка работы пагинатора."""
        address_views_paginator = [
            const.INDEX_URL,
            const.GROUP_POSTS_URL,
            const.PROFILE_AUTH,
        ]
        for reverse_name in address_views_paginator:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertEqual(
                    len(response.context['page_obj']),
                    settings.COUNT_POSTS_PAGES,
                )
                response = self.guest_client.get(reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)
