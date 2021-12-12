from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

import posts.tests.const as const
from posts.models import Comment, Follow, Group, Post, User


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=const.USERNAME_AUTH)
        cls.group = Group.objects.create(
            title=const.GROUP_TITLE,
            slug=const.SLUG,
            description=const.DESCRIPTION,
        )
        uploaded = SimpleUploadedFile(
            name='smoll.gif',
            content=const.SMOLL_GIF,
            content_type='image/gif',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=const.TEXT,
            group=cls.group,
            image=uploaded,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=const.USERNAME_REG)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.post.author)
        self.user_authorized = User.objects.create_user(
            username=const.USERNAME_REG_FOLLOW
        )
        self.guest_authorized = Client()
        self.guest_authorized.force_login(self.user_authorized)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cache.clear()
        post_pk = self.post.pk
        post_detail_url = reverse(
            'posts:post_detail', kwargs={'post_id': post_pk}
        )
        post_edit_url = reverse(
            'posts:post_edit', kwargs={'post_id': post_pk}
        )
        templates_pages_views_func = {
            const.INDEX_URL: const.INDEX_TEMPLATE,
            const.GROUP_POSTS_URL: const.GROUP_POSTS_TEMPLATE,
            const.PROFILE_REG: const.PROFILE_TEMPLATE,
            const.POST_CREATE_URL: const.POST_CREATE_TEMPLATE,
            post_detail_url: const.POST_DETAIL_TEMPLATE,
            post_edit_url: const.POST_CREATE_TEMPLATE,
        }
        for reverse_name, template in templates_pages_views_func.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        cache.clear()
        response = self.author_client.get(const.INDEX_URL)
        first_object = response.context['page_obj'].object_list[0]
        post_text_0 = first_object.text
        post_pub_date_0 = first_object.pub_date
        post_author_0 = first_object.author.username
        post_image_0 = first_object.image
        self.assertEqual(post_text_0, const.TEXT)
        self.assertTrue(post_pub_date_0, True)
        self.assertEqual(post_author_0, const.USERNAME_AUTH)
        self.assertIsNotNone(post_image_0)

    def test_group_posts_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.author_client.get(const.GROUP_POSTS_URL)
        first_object = response.context['page_obj'].object_list[0]
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_group_0, const.GROUP_TITLE)
        self.assertIsNotNone(post_image_0)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.author_client.get(const.PROFILE_AUTH)
        first_object = response.context['page_obj'].object_list[0]
        post_author_0 = first_object.author.username
        post_image_0 = first_object.image
        self.assertEqual(post_author_0, const.USERNAME_AUTH)
        self.assertIsNotNone(post_image_0)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        post_pk = self.post.id
        post_image = self.post.image
        post_detail_url = reverse(
            'posts:post_detail', kwargs={'post_id': post_pk}
        )
        response = self.author_client.get(post_detail_url)
        object_id = response.context['post_object'].pk
        self.assertEqual(object_id, post_pk)
        self.assertIsNotNone(post_image)

    def test_post_group_show(self):
        """Проверка отображения поста с указанной группой."""
        cache.clear()
        address_pages_names = [
            const.INDEX_URL,
            const.GROUP_POSTS_URL,
            const.PROFILE_AUTH,
        ]
        for reverse_name in address_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                listing_address = response.context['page_obj']
                self.assertIn(
                    self.post,
                    listing_address,
                    'Поста группы нет',
                )

    def test_add_comment_authoriz_user(self):
        """Проверка возможности комментировать посты только авторизованным
        пользователем.
        """
        post_pk = self.post.pk
        profile_url = reverse(
            'posts:add_comment',
            kwargs={'post_id': post_pk},
        )
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.guest_client.post(
            profile_url,
            data=form_data,
            follow=True
        )
        self.assertFalse(
            Comment.objects.filter(
                text='Тестовый текст',
            ).exists()
        )
        response = self.authorized_client.post(
            profile_url,
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': post_pk})
        )
        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый текст',
            ).exists()
        )

    def test_work_cache_index(self):
        """Тестируем работу кэша главной страницы."""
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            const.POST_CREATE_URL,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, const.PROFILE_REG)
        response = self.authorized_client.get(const.INDEX_URL)
        self.assertIsNone(response.context)
        cache.clear()
        response = self.authorized_client.get(const.INDEX_URL)
        self.assertEqual(
            response.context['page_obj'].object_list[0].text,
            'Тестовый текст',
        )

    def test_show_new_post_in_posts_lines(self):
        """Проверка отображения нового поста в лентах подписанных и
        неподписанных пользователей.
        """
        Follow.objects.create(
            user=self.user,
            author=self.post.author,
        )
        response = self.guest_authorized.get(const.FOLLOW_URL)
        listing_address = response.context['page_obj']
        self.assertNotIn(
            self.post,
            listing_address,
            'Пост отображается',
        )
        response = self.authorized_client.get(const.FOLLOW_URL)
        listing_address = response.context['page_obj']
        self.assertIn(
            self.post,
            listing_address,
            'Пост не отображается',
        )

    def test_subscription_login_user(self):
        """Проверка возможности подписки авторизованным и
        неавторизованным пользователями.
        """
        self.guest_client.get(const.PROFILE_FOLLOW)
        self.assertFalse(Follow.objects.filter(user=self.user).exists())
        self.author_client.get(const.PROFILE_FOLLOW)
        self.assertTrue(Follow.objects.filter(user=self.post.author).exists())
        follow_count = Follow.objects.all().count()
        self.authorized_client.get(const.PROFILE_FOLLOW)
        self.assertEqual(Follow.objects.all().count(), follow_count)
