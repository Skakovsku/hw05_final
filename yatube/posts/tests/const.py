import tempfile

from django.conf import settings
from django.urls import reverse

GROUP_TITLE = 'Тестовая группа'
SLUG = 'test_slug'
DESCRIPTION = 'Тестовое описание группы'
TEXT = 'Тестовый пост 15 символов'
USERNAME_AUTH = 'auth'
USERNAME_REG = 'Tester'
USERNAME_REG_FOLLOW = 'Tester follow'

INDEX_URL = reverse('posts:index')
GROUP_POSTS_URL = reverse('posts:group_posts', kwargs={'slug': SLUG})
POST_CREATE_URL = reverse('posts:post_create')
PROFILE_AUTH = reverse('posts:profile', kwargs={'username': USERNAME_AUTH})
PROFILE_REG = reverse('posts:profile', kwargs={'username': USERNAME_REG})
PROFILE_FOLLOW = reverse(
    'posts:profile_follow',
    kwargs={'username': USERNAME_REG},
)
PROFILE_UNFOLLOW = reverse(
    'posts:profile_unfollow',
    kwargs={'username': USERNAME_REG},
)
FOLLOW_URL = reverse('posts:follow_index')

INDEX_TEMPLATE = 'posts/index.html'
GROUP_POSTS_TEMPLATE = 'posts/group_list.html'
POST_CREATE_TEMPLATE = 'posts/create_post.html'
PROFILE_TEMPLATE = 'posts/profile.html'
POST_DETAIL_TEMPLATE = 'posts/post_detail.html'
POST_EDIT_TEMPLATE = 'posts/create_post.html'

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

SMOLL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
