import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

import posts.tests.const as const
from posts.forms import CommentForm, PostForm
from posts.models import Comment, Group, Post, User


@override_settings(MEDIA_ROOT=const.TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
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
            group=cls.group,
        )
        cls.form = PostForm()
        cls.form_comment = CommentForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(const.TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(username=const.USERNAME_REG)
        self.author_client = Client()
        self.author_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        post_pk = self.post.pk
        form_data = {
            'text': 'Тестовый текст',
            'group': post_pk,
        }
        response = self.author_client.post(
            const.POST_CREATE_URL,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, const.PROFILE_REG)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=post_pk,
            ).exists()
        )

    def test_creating_post_with_image(self):
        """Форма с IMAGE создает запись в Post."""
        post_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='smoll.gif',
            content=const.SMOLL_GIF,
            content_type='image/gif',
        )
        form_data = {
            'text': 'Тестовый текст',
            'image': uploaded,
        }
        response = self.author_client.post(
            const.POST_CREATE_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, const.PROFILE_REG)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                image='posts/smoll.gif',
            ).exists()
        )

    def test_change_post_in_edit(self):
        """При отправке формы с post_edit пост изменяется."""
        post_count = Post.objects.count()
        post_pk = self.post.pk
        profile_url = reverse('posts:post_edit', kwargs={'post_id': post_pk})
        form_data = {
            'text': 'Текст изменений',
        }
        response = self.author_client.post(
            profile_url,
            data=form_data,
            follow=True
        )
        self.assertNotEqual(response, Post.objects.filter(pk=post_pk))
        self.assertEqual(Post.objects.count(), post_count)

    def test_show_comment_in_post_detail(self):
        """При отправке формы комментарий появляется на странице поста."""
        post_pk = self.post.pk
        profile_url = reverse(
            'posts:add_comment',
            kwargs={'post_id': post_pk},
        )
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.author_client.post(
            profile_url,
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': post_pk})
        )
        self.assertTrue(Comment.objects.filter(text='Тестовый текст'))
