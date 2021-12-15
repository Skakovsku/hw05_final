from django.test import TestCase

import posts.tests.const as const

from ..models import Comment, Follow, Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME_AUTH)
        cls.user_reg = User.objects.create_user(username=const.USERNAME_REG)
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.SLUG,
            description=const.DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=const.TEXT,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text=const.TEST_COMMENT,
        )
        cls.follow = Follow.objects.create(
            user=cls.user_reg,
            author=cls.user,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        comment = PostModelTest.comment
        follow = PostModelTest.follow
        object_names = {
            post: post.text[:15],
            group: group.title,
            comment: comment.text[:15],
            follow: f'Подписка {follow.user} на {follow.author}',
        }
        for name_object, expected_name in object_names.items():
            self.assertEqual(expected_name, str(name_object))
