from django.test import TestCase

import posts.tests.const as const

from ..models import Group, Post, User


class PostModelTest(TestCase):
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

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        expected_object_name_post = post.text[:15]
        self.assertEqual(expected_object_name_post, str(post))
        expected_object_name_group = group.title
        self.assertEqual(expected_object_name_group, str(group))
